"use client";

import Link from "next/link";
import { Server, Wand2 } from "lucide-react";

import { useLatestPrediction } from "@/hooks/use-predictions";
import { formatPercent, formatTemperature } from "@/lib/format";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { StatusBadge } from "@/components/common/status";
import { UsageBar } from "@/components/node/usage-bar";
import { EmptyState } from "@/components/common/state";
import type { ClusterNode } from "@/types";

export function NodeInspector({ node }: { node: ClusterNode | null }) {
  const { data: prediction } = useLatestPrediction(node?.id);

  return (
    <Card className="glass-panel gap-3">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Server className="size-4 text-primary" />
          Node Inspector
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {!node && <EmptyState title="No node selected" description="Click a node in the 3D room." />}
        {node && (
          <>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-foreground">{node.hostname}</p>
                <p className="text-xs text-muted-foreground">{node.ip_address}</p>
              </div>
              <StatusBadge status={node.status} />
            </div>

            <div className="space-y-2">
              <UsageBar label="CPU" value={node.cpu_usage} />
              <UsageBar label="GPU" value={node.gpu_usage} />
              <UsageBar label="Memory" value={node.memory_usage} />
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="rounded-lg border border-border/60 px-2.5 py-2">
                <p className="text-muted-foreground">Temperature</p>
                <p className="font-medium text-foreground">{formatTemperature(node.temperature)}</p>
              </div>
              <div className="rounded-lg border border-border/60 px-2.5 py-2">
                <p className="text-muted-foreground">Power</p>
                <p className="font-medium text-foreground">{node.power_consumption.toFixed(0)}W</p>
              </div>
            </div>

            {prediction && (
              <div className="rounded-lg border border-border/60 bg-muted/30 p-2.5 text-xs">
                <div className="mb-1 flex items-center justify-between">
                  <span className="font-medium text-foreground">{prediction.predicted_label}</span>
                  <span className="font-semibold text-danger">{formatPercent(prediction.risk_score, 0)}</span>
                </div>
                {prediction.explanation && (
                  <p className="text-muted-foreground">{prediction.explanation}</p>
                )}
              </div>
            )}

            {prediction && prediction.risk_score >= 50 && (
              <Button
                size="sm"
                className="w-full"
                render={<Link href={`/migration?predictionId=${prediction.id}`} />}
              >
                <Wand2 className="size-3.5" />
                Open in Migration Center
              </Button>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}
