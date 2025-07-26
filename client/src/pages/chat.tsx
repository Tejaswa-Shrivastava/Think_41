import { useEffect } from "react";
import ChatWindow from "@/components/chat/ChatWindow";
import ConversationSidebar from "@/components/chat/ConversationSidebar";
import { useChatContext } from "@/contexts/ChatContext";
import { useIsMobile } from "@/hooks/use-mobile";

export default function Chat() {
  const { initializeUser } = useChatContext();
  const isMobile = useIsMobile();

  useEffect(() => {
    // Initialize user on app start
    initializeUser();
  }, [initializeUser]);

  return (
    <div className="h-screen flex overflow-hidden">
      <ConversationSidebar />
      
      {/* Sidebar Overlay for Mobile */}
      <div 
        id="sidebarOverlay" 
        className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden hidden"
      />
      
      <ChatWindow />
    </div>
  );
}
