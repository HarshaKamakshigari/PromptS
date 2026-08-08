"use client";

import { useEffect, useRef } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Send, Square } from "lucide-react";

interface ChatInputProps {
  input: string;
  setInput: (value: string) => void;
  onSubmit: () => void;
  onStop: () => void;
  isStreaming: boolean;
}

export function ChatInput({ input, setInput, onSubmit, onStop, isStreaming }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && !isStreaming) {
        onSubmit();
      }
    }
  };

  return (
    <div className="relative flex items-end w-full border border-border rounded-sm bg-background p-2 focus-within:ring-1 focus-within:ring-primary">
      <Textarea
        ref={textareaRef}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Message PromptShield..."
        className="min-h-[40px] w-full resize-none border-0 bg-transparent py-2 px-3 focus-visible:ring-0 text-sm"
        rows={1}
      />
      <div className="flex h-10 items-center justify-center px-2">
        {isStreaming ? (
          <Button 
            size="icon" 
            variant="destructive" 
            className="w-8 h-8 rounded-sm"
            onClick={onStop}
          >
            <Square className="w-4 h-4 fill-current" />
          </Button>
        ) : (
          <Button 
            size="icon" 
            className="w-8 h-8 rounded-sm bg-primary text-primary-foreground hover:bg-primary/90"
            onClick={onSubmit}
            disabled={!input.trim()}
          >
            <Send className="w-4 h-4" />
          </Button>
        )}
      </div>
    </div>
  );
}
