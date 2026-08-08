import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: string;
}

export function StatCard({ title, value, subtitle, trend }: StatCardProps) {
  return (
    <Card className="rounded-sm border-border bg-card shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground mt-1">
          {subtitle}
          {trend && <span className="text-emerald-500 ml-2">{trend}</span>}
        </p>
      </CardContent>
    </Card>
  );
}
