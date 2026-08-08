"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { HealthResponse } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, Server, Cpu, ShieldCheck } from "lucide-react";

export default function SettingsPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    api.getHealth()
      .then(setHealth)
      .catch(console.error);
  }, []);

  return (
    <div className="p-6 max-w-[1200px] mx-auto space-y-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground mt-1 text-sm">
          System configuration and engine status
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="rounded-sm border-border bg-card shadow-sm">
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <Server className="w-4 h-4" />
              Proxy Status
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm">Status</span>
              <div className="flex items-center gap-2 text-sm font-medium">
                {health?.status === "healthy" ? (
                  <><div className="w-2 h-2 rounded-full bg-emerald-500" /> Online</>
                ) : (
                  <><div className="w-2 h-2 rounded-full bg-red-500" /> Offline</>
                )}
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Endpoint</span>
              <span className="text-sm font-mono text-muted-foreground">http://localhost:8000</span>
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-sm border-border bg-card shadow-sm">
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <Activity className="w-4 h-4" />
              Provider
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm">Provider</span>
              <span className="text-sm font-medium capitalize">{health?.provider || "Groq"}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Status</span>
              <div className="flex items-center gap-2 text-sm font-medium">
                <div className="w-2 h-2 rounded-full bg-emerald-500" /> Connected
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Model</span>
              <span className="text-sm font-mono text-muted-foreground">llama-3.3-70b-versatile</span>
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-sm border-border bg-card shadow-sm col-span-1 md:col-span-2">
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <ShieldCheck className="w-4 h-4" />
              Detection Engines
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex justify-between items-center py-2 border-b border-border">
              <div className="space-y-0.5">
                <div className="text-sm font-medium">Semantic Detection</div>
                <div className="text-xs text-muted-foreground">Identify topic drift using embeddings</div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-muted" />
                <span className="text-sm text-muted-foreground">Disabled</span>
              </div>
            </div>

            <div className="flex justify-between items-center py-2 border-b border-border">
              <div className="space-y-0.5">
                <div className="text-sm font-medium">Intent Classification</div>
                <div className="text-xs text-muted-foreground">Detect malicious intent changes</div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-muted" />
                <span className="text-sm text-muted-foreground">Disabled</span>
              </div>
            </div>

            <div className="flex justify-between items-center py-2">
              <div className="space-y-0.5">
                <div className="text-sm font-medium">Risk Engine</div>
                <div className="text-xs text-muted-foreground">Automatic anomaly scoring</div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-muted" />
                <span className="text-sm text-muted-foreground">Disabled</span>
              </div>
            </div>

            <div className="bg-secondary/50 rounded-sm p-4 text-center text-sm text-muted-foreground mt-4">
              Detection engines will be enabled in Phase 2
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
