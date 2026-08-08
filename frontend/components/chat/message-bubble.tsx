import { Message } from "@/types";
import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "flex flex-col gap-2 p-4 rounded-sm border",
        isUser 
          ? "border-border bg-background ml-12" 
          : "border-border bg-secondary/30 mr-12"
      )}
    >
      <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">
        {isUser ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
        {isUser ? "User" : "Assistant"}
      </div>
      <div className="text-sm whitespace-pre-wrap leading-relaxed">
        {message.content}
      </div>
    </div>
  );
}
