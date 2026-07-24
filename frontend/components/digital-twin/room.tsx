"use client";

import { useMemo } from "react";
import { Canvas } from "@react-three/fiber";
import { Grid, OrbitControls } from "@react-three/drei";

import { Rack } from "@/components/digital-twin/rack";
import { MigrationAnimation } from "@/components/digital-twin/migration-animation";
import type { ClusterNode } from "@/types";

const NODES_PER_RACK = 6;
const RACK_SPACING = 1.6;

interface RackLayout {
  key: string;
  label: string;
  position: [number, number, number];
  nodes: ClusterNode[];
}

function buildLayout(nodesByCluster: Map<number, ClusterNode[]>): RackLayout[] {
  const racks: RackLayout[] = [];
  let rackIndex = 0;

  for (const [clusterId, nodes] of nodesByCluster) {
    const chunkCount = Math.max(1, Math.ceil(nodes.length / NODES_PER_RACK));

    for (let c = 0; c < chunkCount; c++) {
      const chunk = nodes.slice(c * NODES_PER_RACK, (c + 1) * NODES_PER_RACK);
      racks.push({
        key: `${clusterId}-${c}`,
        label: `Cluster ${clusterId} · Rack ${c + 1}`,
        position: [rackIndex * RACK_SPACING - 0, 0, 0],
        nodes: chunk,
      });
      rackIndex++;
    }
  }

  const totalWidth = (racks.length - 1) * RACK_SPACING;
  return racks.map((r, i) => ({
    ...r,
    position: [i * RACK_SPACING - totalWidth / 2, 0, 0],
  }));
}

export function Room({
  nodes,
  selectedNodeId,
  onSelectNode,
  riskByNodeId,
  migrationArc,
}: {
  nodes: ClusterNode[];
  selectedNodeId: number | null;
  onSelectNode: (nodeId: number) => void;
  riskByNodeId: Record<number, number>;
  migrationArc?: { sourceNodeId: number; targetNodeId: number } | null;
}) {
  const layout = useMemo(() => {
    const byCluster = new Map<number, ClusterNode[]>();
    for (const node of nodes) {
      const list = byCluster.get(node.cluster_id) ?? [];
      list.push(node);
      byCluster.set(node.cluster_id, list);
    }
    return buildLayout(byCluster);
  }, [nodes]);

  const nodePosition = (nodeId: number): [number, number, number] | null => {
    for (const rack of layout) {
      const idx = rack.nodes.findIndex((n) => n.id === nodeId);
      if (idx !== -1) {
        return [rack.position[0], 0.25 + idx * 0.3, rack.position[2]];
      }
    }
    return null;
  };

  const arcPoints =
    migrationArc &&
    nodePosition(migrationArc.sourceNodeId) &&
    nodePosition(migrationArc.targetNodeId)
      ? {
          from: nodePosition(migrationArc.sourceNodeId)!,
          to: nodePosition(migrationArc.targetNodeId)!,
        }
      : null;

  return (
    <Canvas camera={{ position: [4, 3.2, 6], fov: 42 }} shadows dpr={[1, 1.5]}>
      <color attach="background" args={["#08090b"]} />
      <fog attach="fog" args={["#08090b", 8, 22]} />
      <ambientLight intensity={0.55} />
      <directionalLight position={[5, 6, 4]} intensity={0.9} castShadow />
      <pointLight position={[-4, 3, -3]} intensity={0.4} color="#3987e5" />
      <pointLight position={[4, 3, 3]} intensity={0.35} color="#9085e9" />

      <Grid
        position={[0, -0.02, 0]}
        args={[30, 30]}
        cellSize={0.5}
        cellThickness={0.5}
        cellColor="#1c1f26"
        sectionSize={2.5}
        sectionThickness={1}
        sectionColor="#2a2e38"
        fadeDistance={18}
        infiniteGrid
      />

      {layout.map((rack) => (
        <Rack
          key={rack.key}
          label={rack.label}
          position={rack.position}
          nodes={rack.nodes}
          selectedNodeId={selectedNodeId}
          onSelectNode={onSelectNode}
          riskByNodeId={riskByNodeId}
        />
      ))}

      {arcPoints && <MigrationAnimation from={arcPoints.from} to={arcPoints.to} />}

      <OrbitControls
        enablePan={false}
        minDistance={3}
        maxDistance={14}
        maxPolarAngle={Math.PI / 2.1}
        autoRotate
        autoRotateSpeed={0.4}
      />
    </Canvas>
  );
}
