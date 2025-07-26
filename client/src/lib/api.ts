import { apiRequest } from "./queryClient";
import { type ChatRequest, type ChatResponse, type User, type Conversation, type Message } from "@shared/schema";

export const chatApi = {
  sendMessage: async (data: ChatRequest): Promise<ChatResponse> => {
    const response = await apiRequest("POST", "/api/chat", data);
    return response.json();
  },

  getConversations: async (userId: string): Promise<Conversation[]> => {
    const response = await fetch(`/api/conversations/${userId}`);
    if (!response.ok) throw new Error("Failed to fetch conversations");
    return response.json();
  },

  getMessages: async (conversationId: string): Promise<Message[]> => {
    const response = await fetch(`/api/conversations/${conversationId}/messages`);
    if (!response.ok) throw new Error("Failed to fetch messages");
    return response.json();
  },

  createUser: async (userData: { username: string; email: string }): Promise<User> => {
    const response = await apiRequest("POST", "/api/users", userData);
    return response.json();
  },

  searchProducts: async (query?: string) => {
    const url = query ? `/api/products/search?q=${encodeURIComponent(query)}` : "/api/products/search";
    const response = await fetch(url);
    if (!response.ok) throw new Error("Failed to search products");
    return response.json();
  },
};
