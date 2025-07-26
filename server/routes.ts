import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { chatRequestSchema, type ChatRequest, type ChatResponse } from "@shared/schema";
import { z } from "zod";

// Groq API integration
const GROQ_API_KEY = process.env.GROQ_API_KEY || process.env.GROQ_API_KEY_ENV_VAR || "";
const GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions";

async function generateAIResponse(userMessage: string, conversationContext: string[] = []): Promise<string> {
  if (!GROQ_API_KEY) {
    return "I apologize, but I'm currently unable to process your request. Please ensure the AI service is properly configured.";
  }

  try {
    const messages = [
      {
        role: "system",
        content: `You are a helpful AI assistant for an e-commerce platform. You can help users with:
        - Product recommendations and information
        - Order tracking and support
        - General questions about products and services
        
        Be friendly, helpful, and concise in your responses. If you need more information to help the user, ask clarifying questions.
        If the user asks about products, you can provide general recommendations but let them know they can search the product database for specific items.`
      },
      ...conversationContext.map((msg, index) => ({
        role: index % 2 === 0 ? "user" : "assistant",
        content: msg
      })),
      {
        role: "user",
        content: userMessage
      }
    ];

    const response = await fetch(GROQ_API_URL, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${GROQ_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "llama-3.3-70b-versatile",
        messages,
        max_tokens: 1000,
        temperature: 0.7
      })
    });

    if (!response.ok) {
      console.error("Groq API error:", response.status, await response.text());
      return "I'm experiencing some technical difficulties. Please try again in a moment.";
    }

    const data = await response.json();
    return data.choices[0]?.message?.content || "I'm sorry, I couldn't generate a response. Please try again.";
  } catch (error) {
    console.error("Error calling Groq API:", error);
    return "I'm experiencing some technical difficulties. Please try again in a moment.";
  }
}

function generateConversationTitle(userMessage: string): string {
  const words = userMessage.split(' ').slice(0, 4);
  return words.join(' ') + (userMessage.split(' ').length > 4 ? '...' : '');
}

export async function registerRoutes(app: Express): Promise<Server> {
  // Chat endpoint
  app.post("/api/chat", async (req, res) => {
    try {
      const validatedData = chatRequestSchema.parse(req.body);
      const { userId, message, conversationId } = validatedData;

      // Check if user exists
      const user = await storage.getUser(userId);
      if (!user) {
        return res.status(404).json({ message: "User not found" });
      }

      let conversation;
      
      if (conversationId) {
        // Use existing conversation
        conversation = await storage.getConversation(conversationId);
        if (!conversation) {
          return res.status(404).json({ message: "Conversation not found" });
        }
      } else {
        // Create new conversation
        const title = generateConversationTitle(message);
        conversation = await storage.createConversation({
          userId,
          title
        });
      }

      // Save user message
      const userMessage = await storage.createMessage({
        conversationId: conversation.id,
        content: message,
        sender: "user"
      });

      // Get conversation context for AI
      const previousMessages = await storage.getMessagesByConversationId(conversation.id);
      const contextMessages = previousMessages
        .slice(-10) // Last 10 messages for context
        .map(msg => msg.content);

      // Generate AI response
      const aiContent = await generateAIResponse(message, contextMessages);

      // Save AI message
      const aiMessage = await storage.createMessage({
        conversationId: conversation.id,
        content: aiContent,
        sender: "ai"
      });

      // Update conversation timestamp
      await storage.updateConversationTimestamp(conversation.id);

      const response: ChatResponse = {
        conversationId: conversation.id,
        userMessage: {
          id: userMessage.id,
          content: userMessage.content,
          sender: "user",
          timestamp: userMessage.timestamp.toISOString()
        },
        aiMessage: {
          id: aiMessage.id,
          content: aiMessage.content,
          sender: "ai",
          timestamp: aiMessage.timestamp.toISOString()
        }
      };

      res.json(response);
    } catch (error) {
      console.error("Chat API error:", error);
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid request data", errors: error.errors });
      }
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Get conversations for a user
  app.get("/api/conversations/:userId", async (req, res) => {
    try {
      const { userId } = req.params;
      const conversations = await storage.getConversationsByUserId(userId);
      res.json(conversations);
    } catch (error) {
      console.error("Get conversations error:", error);
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Get messages for a conversation
  app.get("/api/conversations/:conversationId/messages", async (req, res) => {
    try {
      const { conversationId } = req.params;
      const messages = await storage.getMessagesByConversationId(conversationId);
      res.json(messages);
    } catch (error) {
      console.error("Get messages error:", error);
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Create or get user (simple authentication for demo)
  app.post("/api/users", async (req, res) => {
    try {
      const { username, email } = req.body;
      
      if (!username || !email) {
        return res.status(400).json({ message: "Username and email are required" });
      }

      // Check if user exists
      let user = await storage.getUserByEmail(email);
      
      if (!user) {
        // Create new user
        user = await storage.createUser({
          username,
          email,
          password: "demo" // In production, this should be properly hashed
        });
      }

      res.json(user);
    } catch (error) {
      console.error("User creation error:", error);
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Search products
  app.get("/api/products/search", async (req, res) => {
    try {
      const { q } = req.query;
      
      if (!q || typeof q !== "string") {
        const allProducts = await storage.getProducts();
        return res.json(allProducts.slice(0, 20)); // Limit to 20 products
      }

      const products = await storage.searchProducts(q);
      res.json(products);
    } catch (error) {
      console.error("Product search error:", error);
      res.status(500).json({ message: "Internal server error" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
