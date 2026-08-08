"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Metrics, Session } from "@/types";
import { StatCard } from "@/components/dashboard/stat-card";
import { RequestChart } from "@/components/dashboard/request-chart";
import { DriftChartPlaceholder } from "@/components/dashboard/drift-chart";
import { RecentActivity } from "@/components/dashboard/recent-activity";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [m, s] = await Promise.all([
        api.getMetrics(),
        api.getSessions()
      ]);
      setMetrics(m);
      setSessions(s);
    } catch (error) {
      console.error("Failed to fetch dashboard data", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // Poll every 5 seconds
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 max-w-[1600px] mx-auto space-y-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Security Overview</h1>
          <p className="text-muted-foreground mt-1 text-sm">
            Real-time activity through PromptShield
          </p>
        </div>
        <Button 
          variant="outline" 
          size="sm" 
          onClick={fetchData} 
          className="border-border rounded-sm h-8"
        >
          <RefreshCw className={`w-3.5 h-3.5 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard 
          title="Requests" 
          value={metrics?.requests || 0} 
        />
        <StatCard 
          title="Active Sessions" 
          value={metrics?.active_sessions || 0} 
        />
        <StatCard 
          title="Security Events" 
          value={0} 
          subtitle="Detection engine inactive"
        />
        <StatCard 
          title="Avg Latency" 
          value={`${metrics?.average_latency_ms || 0} ms`} 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 h-[520px]">
        {/* Charts Column */}
        <div className="lg:col-span-3 grid grid-cols-1 gap-4 grid-rows-2">
          <RequestChart />
          <DriftChartPlaceholder />
        </div>
        
        {/* Activity Column */}
        <div className="lg:col-span-1 h-full">
          <RecentActivity sessions={sessions} />
        </div>
      </div>
    </div>
  );
}
