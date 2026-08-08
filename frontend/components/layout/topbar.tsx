"use client";

import { usePathname } from "next/navigation";

export function Topbar() {
  const pathname = usePathname();
  
  // Format the path nicely
  const getPageTitle = () => {
    if (pathname === "/dashboard") return "Dashboard";
    if (pathname.startsWith("/chat")) return "Chat";
    if (pathname.startsWith("/sessions")) return "Sessions";
    if (pathname.startsWith("/alerts")) return "Alerts";
    if (pathname.startsWith("/settings")) return "Settings";
    return "Overview";
  };

  return (
    <div className="h-14 border-b border-border bg-background flex items-center justify-between px-6 shrink-0">
      <div className="flex items-center text-sm">
        <span className="text-muted-foreground mr-2">PromptShield</span>
        <span className="text-muted-foreground mr-2">/</span>
        <span className="font-medium">{getPageTitle()}</span>
      </div>

      <div className="flex items-center gap-4 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500" />
          <span className="text-muted-foreground">Proxy Online</span>
        </div>
        <div className="text-muted-foreground border-l border-border pl-4">
          Groq
        </div>
      </div>
    </div>
  );
}
