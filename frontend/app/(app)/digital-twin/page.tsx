"use client";

import { useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { Loader2, Sparkles } from "lucide-react";
import { toast } from "sonner";

import { useNodes } from "@/hooks/use-node";
import { useHighRiskPredictions } from "@/hooks/use-predictions";
import { useMigrationLogStore } from "@/store/migration-log-store";
import { simulatorService } from "@/services/simulator.service";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { EmptyState, ErrorState, LoadingBlock } from "@/components/common/state";
import { NodeInspector } from "@/components/digital-twin/node-inspector";
import { RealityPanel } from "@/components/digital-twin/reality-panel";
import { RecoveryPanel } from "@/components/digital-twin/recovery-panel";

const Room = dynamic(() => import("@/components/digital-twin/room").then((m) => m.Room), {
  ssr: false,
  loading: () => (
    <div className="flex h-full items-center justify-center">
      <Loader2 className="size-6 animate-spin text-primary" />
    </div>
  ),
});

export default function DigitalTwinPage() {
  const { data: nodes, isLoading, isError, refetch } = useNodes();
  const { data: highRisk } = useHighRiskPredictions(50);
  const latestMigration = useMigrationLogStore((s) => s.entries[0]);
  const [selectedNodeId, setSelectedNodeId] = useState<number | null>(null);

  const riskByNodeId = useMemo(() => {
    const map: Record<number, number> = {};
    for (const p of highRisk ?? []) {
      if (!map[p.node_id] || map[p.node_id] < p.risk_score) map[p.node_id] = p.risk_score;
    }
    return map;
  }, [highRisk]);

  const migrationArc = useMemo(() => {
    if (!latestMigration?.result.plan?.target_node) return null;
    const age = Date.now() - new Date(latestMigration.timestamp).getTime();
    if (age > 60_000) return null;
    return {
      sourceNodeId: latestMigration.source_node_id,
      targetNodeId: latestMigration.result.plan.target_node,
    };
  }, [latestMigration]);

  const selectedNode = nodes?.find((n) => n.id === selectedNodeId) ?? null;

  const seedDemoData = async () => {
    try {
      await simulatorService.publish();
      toast.success("Telemetry published — AI pipeline is processing it now.");
      setTimeout(() => refetch(), 1500);
    } catch {
      toast.error("Could not reach the simulator endpoint.");
    }
  };

  return (
    <div>
      <PageHeader
        title="Digital Twin"
        description="Live 3D mirror of your server room — click a node to inspect it."
        actions={
          <Button size="sm" variant="outline" onClick={seedDemoData}>
            <Sparkles className="size-3.5" />
            Seed demo telemetry
          </Button>
        }
      />

      {isLoading && <LoadingBlock rows={4} />}
      {isError && <ErrorState onRetry={() => refetch()} message="Could not load nodes." />}
      {!isLoading && !isError && (!nodes || nodes.length === 0) && (
        <EmptyState
          title="No nodes to visualize"
          description="Register a cluster and nodes first, from the Clusters / Nodes pages."
        />
      )}

      {nodes && nodes.length > 0 && (
        <div className="grid grid-cols-1 gap-4 xl:grid-cols-[1fr_360px]">
          <div className="glass-panel h-[640px] overflow-hidden rounded-xl">
            <Room
              nodes={nodes}
              selectedNodeId={selectedNodeId}
              onSelectNode={setSelectedNodeId}
              riskByNodeId={riskByNodeId}
              migrationArc={migrationArc}
            />
          </div>

          <div className="space-y-4">
            <NodeInspector node={selectedNode} />
            <RealityPanel node={selectedNode} />
            <RecoveryPanel node={selectedNode} />
          </div>
        </div>
      )}
    </div>
  );
}
