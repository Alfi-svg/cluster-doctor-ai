"use client";

import { Edges, Html } from "@react-three/drei";

import { NodeMesh } from "@/components/digital-twin/node-mesh";
import type { ClusterNode } from "@/types";

export function Rack({
  label,
  position,
  nodes,
  selectedNodeId,
  onSelectNode,
  riskByNodeId,
}: {
  label: string;
  position: [number, number, number];
  nodes: ClusterNode[];
  selectedNodeId: number | null;
  onSelectNode: (nodeId: number) => void;
  riskByNodeId: Record<number, number>;
}) {
  const slotHeight = 0.3;
  const height = Math.max(nodes.length * slotHeight + 0.3, 1.2);

  return (
    <group position={position}>
      {/* Rack frame */}
      <mesh position={[0, height / 2, 0]}>
        <boxGeometry args={[1, height, 0.62]} />
        <meshStandardMaterial color="#14161b" roughness={0.85} metalness={0.1} transparent opacity={0.35} />
        <Edges color="#3a3f4a" />
      </mesh>

      {nodes.map((node, i) => (
        <NodeMesh
          key={node.id}
          node={node}
          position={[0, 0.25 + i * slotHeight, 0]}
          selected={selectedNodeId === node.id}
          onSelect={onSelectNode}
          riskScore={riskByNodeId[node.id]}
        />
      ))}

      <Html position={[0, -0.22, 0]} center distanceFactor={9}>
        <div className="pointer-events-none whitespace-nowrap text-[11px] font-medium text-muted-foreground">
          {label}
        </div>
      </Html>
    </group>
  );
}
