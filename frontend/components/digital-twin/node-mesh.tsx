"use client";

import { useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import { Html } from "@react-three/drei";
import type { Mesh } from "three";

import type { ClusterNode } from "@/types";

const STATUS_COLOR: Record<string, string> = {
  ONLINE: "#0ca30c",
  OFFLINE: "#5b6270",
  MAINTENANCE: "#fab219",
  FAILED: "#d03b3b",
};

export function NodeMesh({
  node,
  position,
  selected,
  onSelect,
  riskScore,
}: {
  node: ClusterNode;
  position: [number, number, number];
  selected: boolean;
  onSelect: (nodeId: number) => void;
  riskScore?: number;
}) {
  const meshRef = useRef<Mesh>(null);
  const [hovered, setHovered] = useState(false);

  const isCritical = riskScore !== undefined && riskScore >= 75 && node.status === "ONLINE";
  const color = isCritical ? "#d03b3b" : STATUS_COLOR[node.status] ?? "#5b6270";

  useFrame((state) => {
    if (!meshRef.current) return;
    const targetScale = hovered || selected ? 1.12 : 1;
    meshRef.current.scale.lerp({ x: targetScale, y: targetScale, z: targetScale } as never, 0.15);

    if (isCritical) {
      const pulse = 0.55 + Math.sin(state.clock.elapsedTime * 4) * 0.25;
      (meshRef.current.material as { emissiveIntensity?: number }).emissiveIntensity = pulse;
    }
  });

  return (
    <group position={position}>
      <mesh
        ref={meshRef}
        onClick={(e) => {
          e.stopPropagation();
          onSelect(node.id);
        }}
        onPointerOver={(e) => {
          e.stopPropagation();
          setHovered(true);
        }}
        onPointerOut={() => setHovered(false)}
      >
        <boxGeometry args={[0.82, 0.22, 0.5]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={selected ? 0.9 : 0.35}
          roughness={0.4}
          metalness={0.35}
        />
      </mesh>

      {(hovered || selected) && (
        <Html distanceFactor={8} position={[0, 0.32, 0]} center>
          <div className="pointer-events-none whitespace-nowrap rounded-md border border-border bg-popover px-2 py-1 text-[11px] text-popover-foreground shadow-lg">
            <p className="font-medium">{node.hostname}</p>
            <p className="text-muted-foreground">
              {node.status} · CPU {node.cpu_usage.toFixed(0)}%
              {riskScore !== undefined ? ` · Risk ${riskScore.toFixed(0)}%` : ""}
            </p>
          </div>
        </Html>
      )}
    </group>
  );
}
