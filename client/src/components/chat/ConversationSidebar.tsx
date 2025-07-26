import { Plus, X, MessageSquare, User, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useChatContext } from "@/contexts/ChatContext";
import { useQuery } from "@tanstack/react-query";
import { cn } from "@/lib/utils";

export default function ConversationSidebar() {
  const { 
    currentUser, 
    currentConversation, 
    conversations,
    isSidebarOpen, 
    toggleSidebar, 
    createNewConversation, 
    selectConversation 
  } = useChatContext();

  const formatRelativeTime = (date: string) => {
    const now = new Date();
    const messageDate = new Date(date);
    const diffInHours = Math.floor((now.getTime() - messageDate.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return "now";
    if (diffInHours < 24) return `${diffInHours}h`;
    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays === 1) return "1d";
    if (diffInDays < 7) return `${diffInDays}d`;
    return messageDate.toLocaleDateString();
  };

  return (
    <div 
      className={cn(
        "w-80 bg-white border-r border-slate-200 flex flex-col transform transition-transform duration-300 ease-in-out lg:translate-x-0 fixed lg:relative z-30 h-full",
        isSidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}
    >
      {/* Sidebar Header */}
      <div className="p-6 border-b border-slate-200">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold text-slate-800">AI Assistant</h1>
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={toggleSidebar}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
        <p className="text-sm text-slate-500 mt-1">Powered by Groq LLM</p>
      </div>

      {/* New Conversation Button */}
      <div className="p-4">
        <Button 
          onClick={createNewConversation}
          className="w-full bg-primary text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-600 transition-colors flex items-center justify-center gap-2"
        >
          <Plus className="h-4 w-4" />
          New Conversation
        </Button>
      </div>

      {/* Conversation History */}
      <div className="flex-1 overflow-y-auto">
        <div className="px-4 pb-4">
          <h3 className="text-sm font-medium text-slate-500 mb-3">Recent Conversations</h3>
          
          {conversations.length === 0 ? (
            <div className="text-center py-8">
              <MessageSquare className="h-8 w-8 text-slate-400 mx-auto mb-2" />
              <p className="text-sm text-slate-500">No conversations yet</p>
              <p className="text-xs text-slate-400 mt-1">Start a new conversation to begin</p>
            </div>
          ) : (
            <div className="space-y-2">
              {conversations.map((conversation) => (
                <Card
                  key={conversation.id}
                  className={cn(
                    "p-3 cursor-pointer hover:bg-slate-50 transition-colors border-l-3 border-transparent hover:border-primary",
                    currentConversation?.id === conversation.id && "border-primary bg-slate-50"
                  )}
                  onClick={() => selectConversation(conversation.id)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-800 truncate">
                        {conversation.title}
                      </p>
                      <p className="text-xs text-slate-500 truncate mt-1">
                        Click to view conversation
                      </p>
                    </div>
                    <span className="text-xs text-slate-400 ml-2">
                      {formatRelativeTime(conversation.updatedAt.toString())}
                    </span>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* User Profile Section */}
      <div className="p-4 border-t border-slate-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
            <User className="h-4 w-4 text-white" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-slate-800">
              {currentUser?.username || "Guest"}
            </p>
            <p className="text-xs text-slate-500">
              {currentUser?.email || "guest@example.com"}
            </p>
          </div>
          <Button variant="ghost" size="icon">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
