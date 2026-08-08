"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Session } from "@/types";
import { format } from "date-fns";
import { useRouter } from "next/navigation";

interface RecentActivityProps {
  sessions: Session[];
}

export function RecentActivity({ sessions }: RecentActivityProps) {
  const router = useRouter();

  return (
    <Card className="rounded-sm border-border bg-card shadow-sm col-span-4 lg:col-span-1 h-full">
      <CardHeader>
        <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
          Recent Activity
        </CardTitle>
      </CardHeader>
      <CardContent className="px-0">
        {sessions.length === 0 ? (
          <div className="px-6 py-8 text-center text-sm text-muted-foreground">
            No activity yet.
            <br />
            Start a chat to see telemetry.
          </div>
        ) : (
          <div className="space-y-0">
            {sessions.slice(0, 8).map((session) => (
              <div
                key={session.id}
                onClick={() => router.push(`/sessions/${session.id}`)}
                className="flex items-center justify-between px-6 py-3 border-b border-border hover:bg-secondary/50 cursor-pointer transition-colors text-sm"
              >
                <div className="flex flex-col gap-1">
                  <span className="font-medium">{session.id}</span>
                  <span className="text-xs text-muted-foreground">
                    {format(new Date(session.started_at), "HH:mm:ss")}
                  </span>
                </div>
                <div className="flex flex-col items-end gap-1">
                  <span className="text-xs">{session.model || session.provider}</span>
                  <span className="text-xs text-muted-foreground">
                    {session.request_count} reqs
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
