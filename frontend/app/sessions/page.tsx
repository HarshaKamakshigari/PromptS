"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Session } from "@/types";
import { format } from "date-fns";
import { useRouter } from "next/navigation";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

export default function SessionsPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    api.getSessions()
      .then(setSessions)
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="p-6 max-w-[1200px] mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Sessions</h1>
          <p className="text-muted-foreground mt-1 text-sm">
            All conversations handled by PromptShield
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-2 border border-border rounded-sm px-3 bg-card h-10 w-80">
        <Search className="w-4 h-4 text-muted-foreground" />
        <Input 
          placeholder="Search sessions..." 
          className="border-0 bg-transparent shadow-none focus-visible:ring-0 px-2 h-full text-sm"
        />
      </div>

      <div className="border border-border rounded-sm bg-card overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="border-border hover:bg-transparent">
              <TableHead className="font-semibold text-muted-foreground">Session</TableHead>
              <TableHead className="font-semibold text-muted-foreground">Provider</TableHead>
              <TableHead className="font-semibold text-muted-foreground">Model</TableHead>
              <TableHead className="font-semibold text-muted-foreground">Started At</TableHead>
              <TableHead className="font-semibold text-muted-foreground text-right">Requests</TableHead>
              <TableHead className="font-semibold text-muted-foreground text-right">Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-10 text-muted-foreground">
                  Loading...
                </TableCell>
              </TableRow>
            ) : sessions.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-10 text-muted-foreground">
                  No sessions found.
                </TableCell>
              </TableRow>
            ) : (
              sessions.map((session) => (
                <TableRow 
                  key={session.id} 
                  className="border-border cursor-pointer transition-colors hover:bg-secondary/50"
                  onClick={() => router.push(`/sessions/${session.id}`)}
                >
                  <TableCell className="font-medium font-mono text-sm">{session.id}</TableCell>
                  <TableCell>{session.provider || "Groq"}</TableCell>
                  <TableCell className="text-muted-foreground">{session.model}</TableCell>
                  <TableCell className="text-muted-foreground">
                    {format(new Date(session.started_at), "MMM d, HH:mm:ss")}
                  </TableCell>
                  <TableCell className="text-right font-mono">{session.request_count}</TableCell>
                  <TableCell className="text-right">
                    <div className="inline-flex items-center gap-2 text-xs font-medium border border-border px-2 py-1 rounded-sm bg-background uppercase">
                      <div className="w-2 h-2 rounded-full bg-emerald-500" />
                      {session.status}
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
