"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const MOCK_DATA = [
  { time: "08:00", requests: 12 },
  { time: "08:10", requests: 18 },
  { time: "08:20", requests: 15 },
  { time: "08:30", requests: 25 },
  { time: "08:40", requests: 22 },
  { time: "08:50", requests: 30 },
  { time: "09:00", requests: 45 },
];

export function RequestChart() {
  return (
    <Card className="rounded-sm border-border bg-card shadow-sm col-span-2">
      <CardHeader>
        <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
          Request Activity
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={MOCK_DATA}>
            <XAxis 
              dataKey="time" 
              stroke="#71717A" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="#71717A" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: "#111113", border: "1px solid #27272A", borderRadius: "4px" }}
              itemStyle={{ color: "#F4F4F5" }}
            />
            <Line 
              type="monotone" 
              dataKey="requests" 
              stroke="#F4F4F5" 
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
