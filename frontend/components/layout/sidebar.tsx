"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, MessageSquare, List, ShieldAlert, Settings, ShieldCheck } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Chat", href: "/chat", icon: MessageSquare },
  { name: "Sessions", href: "/sessions", icon: List },
  { name: "Alerts", href: "/alerts", icon: ShieldAlert },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 border-r border-border bg-background flex flex-col h-full shrink-0">
      <div className="h-14 flex items-center px-6 border-b border-border">
        <ShieldCheck className="w-5 h-5 mr-2 text-primary" />
        <span className="font-semibold text-lg tracking-tight">PromptShield</span>
      </div>
      
      <div className="flex-1 py-6 flex flex-col gap-1 px-4 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname.startsWith(item.href);
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
                isActive 
                  ? "bg-secondary text-primary font-medium" 
                  : "text-muted-foreground hover:bg-secondary/50 hover:text-primary"
              )}
            >
              <item.icon className="w-4 h-4" />
              {item.name}
            </Link>
          );
        })}
        
        <div className="mt-8 mb-4 border-t border-border" />
        
        <Link
          href="/settings"
          className={cn(
            "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
            pathname.startsWith("/settings") 
              ? "bg-secondary text-primary font-medium" 
              : "text-muted-foreground hover:bg-secondary/50 hover:text-primary"
          )}
        >
          <Settings className="w-4 h-4" />
          Settings
        </Link>
      </div>

      <div className="p-4 border-t border-border mt-auto">
        <div className="flex items-center gap-2 mb-1">
          <div className="w-2 h-2 rounded-full bg-emerald-500" />
          <span className="text-xs font-medium">Groq Connected</span>
        </div>
        <div className="text-xs text-muted-foreground ml-4">Proxy Online</div>
      </div>
    </div>
  );
}
