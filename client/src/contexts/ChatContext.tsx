import React, { createContext, useContext, useState, useCallback } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { type User, type Conversation, type Message, type ChatResponse } from "@shared/schema";
import { apiRequest } from "@/lib/queryClient";
import { useIsMobile } from "@/hooks/use-mobile";

interface ChatContextType {
  // State
  currentUser: User | null;
  currentConversation: Conversation | null;
  conversations: Conversation[];
  messages: Message[];
  isLoading: boolean;
  isSidebarOpen: boolean;

  // Actions
  initializeUser: () => void;
  sendMessage: (message: string) => Promise<void>;
  createNewConversation: () => void;
  selectConversation: (conversationId: string) => void;
  clearCurrentConversation: () => void;
  toggleSidebar: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export function useChatContext() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error("useChatContext must be used within a ChatProvider");
  }
  return context;
}

interface ChatProviderProps {
  children: React.ReactNode;
}

export function ChatProvider({ children }: ChatProviderProps) {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const isMobile = useIsMobile();
  const queryClient = useQueryClient();

  // Initialize or get user
  const initializeUser = useCallback(async () => {
    try {
      // For demo purposes, create/get a default user
      const response = await apiRequest("POST", "/api/users", {
        username: "Demo User",
        email: "demo@example.com"
      });
      
      const user = await response.json();
      setCurrentUser(user);
    } catch (error) {
      console.error("Failed to initialize user:", error);
    }
  }, []);

  // Get conversations for current user
  const { data: conversations = [] } = useQuery<Conversation[]>({
    queryKey: ["/api/conversations", currentUser?.id],
    enabled: !!currentUser?.id,
  });

  // Send message mutation
  const sendMessageMutation = useMutation({
    mutationFn: async (messageData: { message: string }) => {
      if (!currentUser) throw new Error("No user found");
      
      const response = await apiRequest("POST", "/api/chat", {
        userId: currentUser.id,
        message: messageData.message,
        conversationId: currentConversation?.id,
      });
      
      return response.json() as Promise<ChatResponse>;
    },
    onSuccess: (data) => {
      // Add both user and AI messages to the current messages
      const newUserMessage: Message = {
        id: data.userMessage.id,
        conversationId: data.conversationId,
        content: data.userMessage.content,
        sender: "user",
        timestamp: new Date(data.userMessage.timestamp),
      };
      
      const newAIMessage: Message = {
        id: data.aiMessage.id,
        conversationId: data.conversationId,
        content: data.aiMessage.content,
        sender: "ai",
        timestamp: new Date(data.aiMessage.timestamp),
      };

      setMessages(prev => [...prev, newUserMessage, newAIMessage]);

      // Update current conversation if it's new
      if (!currentConversation) {
        queryClient.invalidateQueries({ 
          queryKey: ["/api/conversations", currentUser?.id] 
        });
      }

      // Close sidebar on mobile after sending message
      if (isMobile) {
        setIsSidebarOpen(false);
      }
    },
  });

  // Get messages for current conversation
  const { isLoading: isLoadingMessages } = useQuery<Message[]>({
    queryKey: ["/api/conversations", currentConversation?.id, "messages"],
    enabled: !!currentConversation?.id,
    queryFn: async () => {
      const response = await fetch(`/api/conversations/${currentConversation?.id}/messages`);
      if (!response.ok) throw new Error("Failed to fetch messages");
      const data = await response.json();
      setMessages(data);
      return data;
    },
  });

  const sendMessage = useCallback(async (message: string) => {
    await sendMessageMutation.mutateAsync({ message });
  }, [sendMessageMutation]);

  const createNewConversation = useCallback(() => {
    setCurrentConversation(null);
    setMessages([]);
    if (isMobile) {
      setIsSidebarOpen(false);
    }
  }, [isMobile]);

  const selectConversation = useCallback((conversationId: string) => {
    const conversation = conversations.find(c => c.id === conversationId);
    if (conversation) {
      setCurrentConversation(conversation);
      if (isMobile) {
        setIsSidebarOpen(false);
      }
    }
  }, [conversations, isMobile]);

  const clearCurrentConversation = useCallback(() => {
    setMessages([]);
  }, []);

  const toggleSidebar = useCallback(() => {
    setIsSidebarOpen(prev => !prev);
  }, []);

  const value: ChatContextType = {
    // State
    currentUser,
    currentConversation,
    conversations,
    messages,
    isLoading: sendMessageMutation.isPending || isLoadingMessages,
    isSidebarOpen,

    // Actions
    initializeUser,
    sendMessage,
    createNewConversation,
    selectConversation,
    clearCurrentConversation,
    toggleSidebar,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
}
