import { useEffect, useRef } from "react";
import { MessageSquare } from "lucide-react";
import Message from "./Message";
import { useChatContext } from "@/contexts/ChatContext";
import { Card } from "@/components/ui/card";

export default function MessageList() {
  const { messages, isLoading } = useChatContext();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.length === 0 ? (
        /* Welcome Message */
        <div className="flex justify-center">
          <Card className="bg-white rounded-lg p-4 shadow-sm border border-slate-200 max-w-md text-center">
            <div className="w-12 h-12 bg-secondary rounded-full mx-auto mb-3 flex items-center justify-center">
              <MessageSquare className="h-6 w-6 text-white" />
            </div>
            <h3 className="font-semibold text-slate-800 mb-2">Welcome to AI Assistant</h3>
            <p className="text-sm text-slate-600">
              I'm here to help you with product information, orders, and general questions. 
              How can I assist you today?
            </p>
          </Card>
        </div>
      ) : (
        messages.map((message) => (
          <Message key={message.id} message={message} />
        ))
      )}

      {/* Typing Indicator */}
      {isLoading && (
        <div className="flex justify-start animate-fade-in">
          <div className="flex gap-3 max-w-xs lg:max-w-2xl">
            <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0 mt-1">
              <MessageSquare className="h-4 w-4 text-white" />
            </div>
            <div>
              <div className="bg-ai-message rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-slate-500 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-slate-500 rounded-full animate-pulse" style={{animationDelay: "0.2s"}}></div>
                  <div className="w-2 h-2 bg-slate-500 rounded-full animate-pulse" style={{animationDelay: "0.4s"}}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}
