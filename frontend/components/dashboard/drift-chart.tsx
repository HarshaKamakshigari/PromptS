"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function DriftChartPlaceholder() {
  return (
    <Card className="rounded-sm border-border bg-card shadow-sm col-span-2">
      <CardHeader>
        <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
          Drift Monitoring
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[250px] flex flex-col items-center justify-center text-center">
        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">Detection engine not active</p>
          <div className="text-xs text-muted-foreground/50 space-y-1">
            <p>Semantic drift</p>
            <p>Intent drift</p>
            <p>Risk score</p>
          </div>
          <p className="text-xs text-primary mt-4 font-medium px-2 py-1 bg-secondary rounded-sm">
            Coming in Phase 2
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
