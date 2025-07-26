import { Check, MessageSquare } from "lucide-react";
import { type Message as MessageType } from "@shared/schema";

interface MessageProps {
  message: MessageType;
}

export default function Message({ message }: MessageProps) {
  const isUser = message.sender === "user";
  const timestamp = new Date(message.timestamp).toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });

  if (isUser) {
    return (
      <div className="flex justify-end animate-fade-in">
        <div className="max-w-xs lg:max-w-md">
          <div className="bg-user-message text-white rounded-2xl rounded-br-md px-4 py-3 shadow-sm">
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          </div>
          <div className="flex items-center justify-end gap-1 mt-1">
            <span className="text-xs text-slate-500">{timestamp}</span>
            <Check className="h-3 w-3 text-emerald-500" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start animate-fade-in">
      <div className="flex gap-3 max-w-xs lg:max-w-2xl">
        <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0 mt-1">
          <MessageSquare className="h-4 w-4 text-white" />
        </div>
        <div>
          <div className="bg-ai-message rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
            <p className="text-sm text-slate-800 whitespace-pre-wrap">{message.content}</p>
          </div>
          <div className="flex items-center gap-1 mt-1">
            <span className="text-xs text-slate-500">{timestamp}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
