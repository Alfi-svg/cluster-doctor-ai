import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { HealingRunResult, MigrationStartResponse } from "@/types";

class MigrationService {
  /**
   * Runs the full Prediction -> Safe Target -> Migration -> Checkpoint
   * -> Recovery pipeline for a given prediction. `prediction` must
   * include at least `cluster_id` and `node_id`.
   */
  async start(prediction: {
    cluster_id: number;
    node_id: number;
  }): Promise<HealingRunResult> {
    const response = await api.post<MigrationStartResponse>(
      API_ENDPOINTS.migration.start,
      prediction
    );
    return response.data.result;
  }

  /** Backend TODO — always returns []. Kept for completeness/demo. */
  async history(): Promise<unknown[]> {
    const response = await api.get<{ success: boolean; history: unknown[] }>(
      API_ENDPOINTS.migration.history
    );
    return response.data.history;
  }

  /** Backend TODO — always returns {status:"completed"}. */
  async details(migrationId: string): Promise<{ migration_id: string; status: string }> {
    const response = await api.get<{
      success: boolean;
      data: { migration_id: string; status: string };
    }>(`${API_ENDPOINTS.migration.byId}/${migrationId}`);
    return response.data.data;
  }
}

export const migrationService = new MigrationService();
