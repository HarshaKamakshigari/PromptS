"use client";

import { useState, useRef, useEffect } from "react";
import { MessageBubble } from "@/components/chat/message-bubble";
import { ChatInput } from "@/components/chat/chat-input";
import { Message, SessionDetail } from "@/types";
import { streamChatResponse } from "@/lib/chat";
import { api } from "@/lib/api";
import { ShieldCheck, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "system", content: "You are a helpful assistant." }
  ]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [sessionDetail, setSessionDetail] = useState<SessionDetail | null>(null);
  const [model] = useState("llama-3.3-70b-versatile");
  
  const abortControllerRef = useRef<AbortController | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const updateTelemetry = async (sid: string) => {
    try {
      const detail = await api.getSession(sid);
      setSessionDetail(detail);
    } catch (e) {
      console.error("Failed to load telemetry", e);
    }
  };

  const handleSubmit = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input.trim() };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput("");
    setIsStreaming(true);

    abortControllerRef.current = new AbortController();

    // Start with empty assistant message
    setMessages([...newMessages, { role: "assistant", content: "" }]);

    await streamChatResponse({
      model,
      messages: newMessages,
      ps_session_id: sessionId || undefined,
      signal: abortControllerRef.current.signal,
      onChunk: (chunk) => {
        setMessages((prev) => {
          const updated = [...prev];
          const lastIndex = updated.length - 1;
          updated[lastIndex] = {
            ...updated[lastIndex],
            content: updated[lastIndex].content + chunk,
          };
          return updated;
        });
      },
      onDone: () => {
        setIsStreaming(false);
        // Assuming backend handles request ID as session ID if none passed initially
        // Let's fetch latest sessions to find ours if we don't have the ID yet
        if (!sessionId) {
          api.getSessions().then(sessions => {
            if (sessions.length > 0) {
              const sid = sessions[0].id;
              setSessionId(sid);
              updateTelemetry(sid);
            }
          });
        } else {
          updateTelemetry(sessionId);
        }
      },
      onError: (error) => {
        console.error(error);
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: `\n\n[Error: ${error}]` }
        ]);
        setIsStreaming(false);
      }
    });
  };

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  };

  const handleNewSession = () => {
    setSessionId(null);
    setSessionDetail(null);
    setMessages([{ role: "system", content: "You are a helpful assistant." }]);
  };

  return (
    <div className="flex h-full w-full">
      {/* Left Panel: Chat Interface */}
      <div className="flex-1 flex flex-col h-full border-r border-border">
        {/* Chat Header */}
        <div className="h-14 flex items-center justify-between px-6 border-b border-border shrink-0">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500" />
              <span className="text-xs text-muted-foreground font-medium">Groq Connected</span>
            </div>
            <span className="text-xs border border-border px-2 py-0.5 rounded-sm bg-secondary">
              {model}
            </span>
          </div>
          <Button variant="outline" size="sm" onClick={handleNewSession} className="h-8 rounded-sm">
            <Plus className="w-3.5 h-3.5 mr-2" />
            New Session
          </Button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-6">
          {messages.map((msg, i) => (
            <MessageBubble key={i} message={msg} />
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-6 bg-background border-t border-border">
          <ChatInput 
            input={input}
            setInput={setInput}
            onSubmit={handleSubmit}
            onStop={handleStop}
            isStreaming={isStreaming}
          />
        </div>
      </div>

      {/* Right Panel: Telemetry */}
      <div className="w-80 bg-card flex flex-col h-full shrink-0">
        <div className="h-14 flex items-center px-6 border-b border-border shrink-0">
          <span className="text-sm font-semibold tracking-tight uppercase text-muted-foreground">Session Telemetry</span>
        </div>
        
        <div className="p-6 space-y-8 overflow-y-auto">
          {sessionId ? (
            <>
              <div>
                <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Session ID</h3>
                <div className="font-mono text-sm bg-secondary px-3 py-2 rounded-sm border border-border">
                  {sessionId}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Provider</h3>
                  <div className="text-sm">Groq</div>
                </div>
                <div>
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Status</h3>
                  <div className="text-sm flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                    Active
                  </div>
                </div>
                <div>
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Requests</h3>
                  <div className="text-sm font-mono">{sessionDetail?.session?.request_count || 0}</div>
                </div>
                <div>
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Messages</h3>
                  <div className="text-sm font-mono">{sessionDetail?.messages?.length || messages.length}</div>
                </div>
              </div>

              <div className="pt-4 border-t border-border">
                <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-4 flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4" />
                  Security Risk
                </h3>
                
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span>Overall Risk</span>
                      <span className="font-mono">{(sessionDetail?.session?.risk_score || 0).toFixed(2)}</span>
                    </div>
                    <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden">
                      <div className="h-full bg-emerald-500 w-[5%]" />
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-xs mb-1 text-muted-foreground">
                      <span>Semantic drift</span>
                      <span className="font-mono">0.00</span>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-xs mb-1 text-muted-foreground">
                      <span>Intent drift</span>
                      <span className="font-mono">0.00</span>
                    </div>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="text-sm text-muted-foreground text-center py-10">
              Session not started.<br/>Send a message to begin.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
