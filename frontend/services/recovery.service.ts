import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type {
  RecoveryHistoryResponse,
  RecoveryStartResponse,
  RecoveryStatusResponse,
} from "@/types";

interface Envelope<T> {
  success: boolean;
  data: T;
}

/**
 * `/recovery/*` is a thin, hardcoded stub on the backend today
 * (no persistence, canned responses). It's exposed here as-is —
 * the Recovery Center page pairs it with the richer, real
 * `recovery` object returned by `migration.service.start()`.
 */
class RecoveryService {
  async start(nodeId: number | string): Promise<RecoveryStartResponse> {
    const response = await api.post<Envelope<RecoveryStartResponse>>(
      API_ENDPOINTS.recovery.start(nodeId)
    );
    return response.data.data;
  }

  async status(nodeId: number | string): Promise<RecoveryStatusResponse> {
    const response = await api.get<Envelope<RecoveryStatusResponse>>(
      API_ENDPOINTS.recovery.status(nodeId)
    );
    return response.data.data;
  }

  async history(nodeId: number | string): Promise<RecoveryHistoryResponse> {
    const response = await api.get<Envelope<RecoveryHistoryResponse>>(
      API_ENDPOINTS.recovery.history(nodeId)
    );
    return response.data.data;
  }
}

export const recoveryService = new RecoveryService();
