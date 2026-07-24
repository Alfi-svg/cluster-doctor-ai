import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { RealityCompareResult, RealitySummary } from "@/types";

interface Envelope<T> {
  success: boolean;
  data: T;
}

class RealityService {
  /**
   * Compare live telemetry against the Digital Twin's last predicted
   * snapshot for a node. `telemetry` should carry at minimum
   * { cpu, memory, temperature } — the only keys the backend reads.
   */
  async compare(
    nodeId: string,
    telemetry: { cpu: number; memory: number; temperature: number }
  ): Promise<RealityCompareResult> {
    const response = await api.post<Envelope<RealityCompareResult>>(
      API_ENDPOINTS.reality.compare(nodeId),
      { telemetry }
    );
    return response.data.data;
  }

  /**
   * The backend's own `/reality/summary` is a hardcoded stub
   * (always {0,0,0}) — callers should prefer aggregating real
   * `compare()` results across nodes instead of relying on this.
   */
  async rawSummary(): Promise<RealitySummary> {
    const response = await api.get<Envelope<RealitySummary>>(
      API_ENDPOINTS.reality.summary
    );
    return response.data.data;
  }
}

export const realityService = new RealityService();
