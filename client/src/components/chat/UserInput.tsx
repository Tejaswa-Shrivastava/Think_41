import { useState, useRef, useEffect } from "react";
import { Send, Paperclip, Search, Package, MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useChatContext } from "@/contexts/ChatContext";
import { useToast } from "@/hooks/use-toast";

export default function UserInput() {
  const [inputValue, setInputValue] = useState("");
  const [error, setError] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { sendMessage, isLoading } = useChatContext();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputValue.trim() || isLoading) return;

    setError("");
    const message = inputValue.trim();
    setInputValue("");

    try {
      await sendMessage(message);
    } catch (error) {
      console.error("Error sending message:", error);
      setError("Failed to send message. Please try again.");
      toast({
        title: "Error",
        description: "Failed to send message. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleQuickAction = (action: string) => {
    let text = "";
    switch (action) {
      case "product-search":
        text = "Help me find products for ";
        break;
      case "order-status":
        text = "Check the status of my order #";
        break;
      case "support":
        text = "I need help with ";
        break;
    }
    
    setInputValue(text);
    textareaRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = Math.min(textarea.scrollHeight, 128) + "px";
    }
  }, [inputValue]);

  return (
    <div className="bg-white border-t border-slate-200 p-4">
      <form onSubmit={handleSubmit} className="flex gap-3 items-end">
        <div className="flex-1">
          <div className="relative">
            <Textarea
              ref={textareaRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message here..."
              className="w-full resize-none border border-slate-300 rounded-xl px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all max-h-32 min-h-[48px]"
              rows={1}
              disabled={isLoading}
            />
            
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="absolute right-3 top-3 p-1 text-slate-400 hover:text-slate-600"
              title="Attach file"
            >
              <Paperclip className="h-4 w-4" />
            </Button>
          </div>
          
          {/* Quick Actions */}
          <div className="flex gap-2 mt-2">
            <Button
              type="button"
              variant="secondary"
              size="sm"
              className="text-xs px-3 py-1 h-6"
              onClick={() => handleQuickAction("product-search")}
            >
              <Search className="h-3 w-3 mr-1" />
              Find Products
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              className="text-xs px-3 py-1 h-6"
              onClick={() => handleQuickAction("order-status")}
            >
              <Package className="h-3 w-3 mr-1" />
              Check Order
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              className="text-xs px-3 py-1 h-6"
              onClick={() => handleQuickAction("support")}
            >
              <MessageCircle className="h-3 w-3 mr-1" />
              Get Support
            </Button>
          </div>
        </div>
        
        <Button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className="bg-primary text-white p-3 rounded-xl hover:bg-indigo-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[48px]"
        >
          <Send className="h-4 w-4" />
        </Button>
      </form>
      
      {/* Error Message Display */}
      {error && (
        <div className="mt-2 p-3 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center gap-2">
            <MessageCircle className="h-4 w-4 text-red-500" />
            <span className="text-sm text-red-700">{error}</span>
          </div>
        </div>
      )}
    </div>
  );
}
