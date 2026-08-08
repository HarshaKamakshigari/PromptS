"use client";

import { ShieldAlert } from "lucide-react";

export default function AlertsPage() {
  return (
    <div className="p-6 max-w-[1200px] mx-auto space-y-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Security Alerts</h1>
          <p className="text-muted-foreground mt-1 text-sm">
            Threats and anomalies detected in PromptShield sessions
          </p>
        </div>
      </div>

      <div className="flex flex-col items-center justify-center border border-border rounded-sm bg-card py-32 px-4 text-center">
        <div className="w-16 h-16 rounded-full bg-secondary flex items-center justify-center mb-6">
          <ShieldAlert className="w-8 h-8 text-muted-foreground" />
        </div>
        <h2 className="text-lg font-semibold mb-2">No security alerts</h2>
        <p className="text-muted-foreground text-sm max-w-md">
          PromptShield has not detected any security events yet.
          Detection monitoring will appear here when the Phase 2 engine is enabled.
        </p>
      </div>
    </div>
  );
}
