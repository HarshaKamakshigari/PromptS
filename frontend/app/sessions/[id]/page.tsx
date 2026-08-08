"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { SessionDetail } from "@/types";
import { format } from "date-fns";
import { ArrowLeft, Clock, ShieldCheck, Database, Server } from "lucide-react";
import { Button } from "@/components/ui/button";
import { MessageBubble } from "@/components/chat/message-bubble";

export default function SessionDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [detail, setDetail] = useState<SessionDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    api.getSession(id)
      .then(setDetail)
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, [id]);

  if (isLoading) {
    return <div className="p-8 text-muted-foreground">Loading session {id}...</div>;
  }

  if (!detail) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold">Session not found</h1>
        <Button variant="link" onClick={() => router.push("/sessions")} className="mt-4 px-0">
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to sessions
        </Button>
      </div>
    );
  }

  const { session, messages } = detail;

  return (
    <div className="flex h-full w-full">
      {/* Left Panel: Conversation */}
      <div className="flex-1 flex flex-col h-full border-r border-border">
        <div className="h-14 flex items-center px-6 border-b border-border shrink-0 gap-4">
          <Button variant="ghost" size="icon" onClick={() => router.push("/sessions")} className="h-8 w-8 rounded-sm">
            <ArrowLeft className="w-4 h-4" />
          </Button>
          <span className="font-semibold">Conversation</span>
        </div>
        
        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-6 bg-background">
          {messages.length === 0 ? (
            <div className="text-muted-foreground text-center py-10">No messages recorded.</div>
          ) : (
            messages.map((msg, i) => (
              <MessageBubble key={i} message={msg} />
            ))
          )}
        </div>
      </div>

      {/* Right Panel: Metadata & Timeline */}
      <div className="w-96 bg-card flex flex-col h-full shrink-0">
        <div className="h-14 flex items-center px-6 border-b border-border shrink-0">
          <span className="text-sm font-semibold tracking-tight uppercase text-muted-foreground">
            Session Details
          </span>
        </div>

        <div className="p-6 space-y-8 overflow-y-auto">
          {/* Status badge */}
          <div className="flex items-center gap-3">
            <div className="inline-flex items-center gap-2 text-sm font-medium border border-border px-3 py-1.5 rounded-sm bg-background uppercase">
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
              {session.status}
            </div>
            <span className="text-xs text-muted-foreground font-mono">{session.id}</span>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground uppercase tracking-wider font-semibold">
                <Server className="w-3.5 h-3.5" /> Provider
              </div>
              <div className="text-sm">{session.provider || "Groq"}</div>
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground uppercase tracking-wider font-semibold">
                <Database className="w-3.5 h-3.5" /> Model
              </div>
              <div className="text-sm">{session.model}</div>
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground uppercase tracking-wider font-semibold">
                <Clock className="w-3.5 h-3.5" /> Started
              </div>
              <div className="text-sm">{format(new Date(session.started_at), "HH:mm:ss")}</div>
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground uppercase tracking-wider font-semibold">
                <ShieldCheck className="w-3.5 h-3.5" /> Risk Score
              </div>
              <div className="text-sm font-mono">{session.risk_score.toFixed(2)}</div>
            </div>
          </div>

          <div className="border-t border-border pt-6">
            <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-4">
              Request Timeline
            </h3>
            <div className="space-y-3">
              <div className="text-sm text-muted-foreground flex justify-between">
                <span>Total requests</span>
                <span className="font-mono text-foreground">{session.request_count}</span>
              </div>
              <div className="text-sm text-muted-foreground flex justify-between">
                <span>Last activity</span>
                <span className="font-mono text-foreground">
                  {format(new Date(session.last_activity), "HH:mm:ss")}
                </span>
              </div>
            </div>
          </div>
          
          <div className="border-t border-border pt-6">
            <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-4">
              Drift Monitoring
            </h3>
            <div className="bg-background border border-border p-4 rounded-sm text-center">
              <p className="text-sm text-muted-foreground mb-2">Detection engine inactive.</p>
              <p className="text-xs text-primary/70">Chart will appear here in Phase 2.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
