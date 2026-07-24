"use client";

import { useMemo, useState } from "react";
import { RefreshCcw } from "lucide-react";

import { useNodes } from "@/hooks/use-node";
import { useLatestTelemetry, useTelemetryHistory } from "@/hooks/use-telemetry";
import { formatPercent, formatTemperature } from "@/lib/format";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { LiveTelemetryChart } from "@/components/telemetry/live-telemetry-chart";
import { EmptyState, ErrorState, LoadingBlock } from "@/components/common/state";

const RANGE_MS = 30 * 60 * 1000;

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="glass-panel rounded-xl px-4 py-3 text-center">
      <p className="text-lg font-semibold tabular-nums text-foreground">{value}</p>
      <p className="text-[11px] text-muted-foreground">{label}</p>
    </div>
  );
}

export default function TelemetryPage() {
  const { data: nodes, isLoading: loadingNodes } = useNodes();
  const [nodeId, setNodeId] = useState<number | undefined>();

  const activeNodeId = nodeId ?? nodes?.find((n) => n.status === "ONLINE")?.id ?? nodes?.[0]?.id;
  const activeNode = nodes?.find((n) => n.id === activeNodeId);

  const { data: latest } = useLatestTelemetry(activeNodeId);

  const [now] = useState(() => Date.now());
  const startTime = new Date(now - RANGE_MS).toISOString();
  const endTime = new Date(now).toISOString();

  const { data: history, isLoading, isError, refetch } = useTelemetryHistory(
    activeNodeId,
    startTime,
    endTime
  );

  const chartData = useMemo(
    () =>
      (history ?? []).map((t) => ({
        time: new Date(t.recorded_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        cpu: t.cpu_usage,
        gpu: t.gpu_usage,
        ram: t.ram_usage,
        network_in: t.network_in,
        network_out: t.network_out,
        latency: t.latency,
      })),
    [history]
  );

  return (
    <div>
      <PageHeader
        title="Telemetry"
        description="Raw and historical metrics streamed from every node."
        actions={
          <>
            <Select
              value={activeNodeId ? String(activeNodeId) : ""}
              onValueChange={(v) => setNodeId(Number(v))}
            >
              <SelectTrigger className="w-56">
                <SelectValue placeholder="Select node" />
              </SelectTrigger>
              <SelectContent>
                {nodes?.map((n) => (
                  <SelectItem key={n.id} value={String(n.id)}>
                    {n.hostname}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button variant="outline" size="sm" onClick={() => refetch()}>
              <RefreshCcw className="size-3.5" />
              Refresh
            </Button>
          </>
        }
      />

      {loadingNodes && <LoadingBlock rows={2} />}
      {!loadingNodes && !activeNode && (
        <EmptyState title="No nodes available" description="Register a node to see telemetry." />
      )}

      {activeNode && (
        <>
          <div className="mb-5 grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
            <Stat label="CPU" value={formatPercent(latest?.cpu_usage)} />
            <Stat label="GPU" value={formatPercent(latest?.gpu_usage)} />
            <Stat label="RAM" value={formatPercent(latest?.ram_usage)} />
            <Stat label="Disk" value={formatPercent(latest?.disk_usage)} />
            <Stat label="CPU Temp" value={formatTemperature(latest?.cpu_temperature)} />
            <Stat label="GPU Temp" value={formatTemperature(latest?.gpu_temperature)} />
            <Stat label="Latency" value={latest ? `${latest.latency.toFixed(0)}ms` : "—"} />
          </div>

          <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
            <Card className="glass-panel">
              <CardHeader>
                <CardTitle>Compute Usage (last 30 min)</CardTitle>
              </CardHeader>
              <CardContent>
                {isLoading && <LoadingBlock rows={1} />}
                {isError && <ErrorState onRetry={() => refetch()} message="Could not load history." />}
                {!isLoading && !isError && chartData.length === 0 && (
                  <EmptyState title="No telemetry recorded in this window" />
                )}
                {chartData.length > 0 && (
                  <LiveTelemetryChart
                    data={chartData}
                    series={[
                      { key: "cpu", label: "CPU", color: "var(--chart-1)" },
                      { key: "gpu", label: "GPU", color: "var(--chart-2)" },
                      { key: "ram", label: "RAM", color: "var(--chart-3)" },
                    ]}
                  />
                )}
              </CardContent>
            </Card>

            <Card className="glass-panel">
              <CardHeader>
                <CardTitle>Network Throughput (last 30 min)</CardTitle>
              </CardHeader>
              <CardContent>
                {chartData.length > 0 && (
                  <LiveTelemetryChart
                    data={chartData}
                    series={[
                      { key: "network_in", label: "Inbound", color: "var(--chart-1)" },
                      { key: "network_out", label: "Outbound", color: "var(--chart-2)" },
                    ]}
                    yDomain={[0, "dataMax + 10"]}
                  />
                )}
              </CardContent>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}
