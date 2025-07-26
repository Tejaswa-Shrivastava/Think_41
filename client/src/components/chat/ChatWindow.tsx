import { MessageSquare, Trash2, Download } from "lucide-react";
import MessageList from "./MessageList";
import UserInput from "./UserInput";
import { useChatContext } from "@/contexts/ChatContext";
import { Button } from "@/components/ui/button";

export default function ChatWindow() {
  const { 
    currentConversation, 
    toggleSidebar, 
    clearCurrentConversation 
  } = useChatContext();

  return (
    <div className="flex-1 flex flex-col min-w-0">
      {/* Chat Header */}
      <div className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={toggleSidebar}
          >
            <MessageSquare className="h-5 w-5" />
          </Button>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center">
              <MessageSquare className="h-4 w-4 text-white" />
            </div>
            <div>
              <h2 className="font-semibold text-slate-800">
                {currentConversation?.title || "AI Assistant"}
              </h2>
              <p className="text-sm text-slate-500">Online</p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={clearCurrentConversation}
            title="Clear conversation"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            title="Export conversation"
          >
            <Download className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <MessageList />
      <UserInput />
    </div>
  );
}
