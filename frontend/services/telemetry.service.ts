import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { Telemetry, TelemetryCreateInput } from "@/types";

class TelemetryService {
  async create(data: TelemetryCreateInput): Promise<Telemetry> {
    const response = await api.post<Telemetry>(API_ENDPOINTS.telemetry.create, data);
    return response.data;
  }

  async get(id: number | string): Promise<Telemetry> {
    const response = await api.get<Telemetry>(`${API_ENDPOINTS.telemetry.byId}/${id}`);
    return response.data;
  }

  async latest(nodeId: number | string): Promise<Telemetry> {
    const response = await api.get<Telemetry>(
      `${API_ENDPOINTS.telemetry.latest}/${nodeId}`
    );
    return response.data;
  }

  async history(
    nodeId: number | string,
    startTime: string,
    endTime: string
  ): Promise<Telemetry[]> {
    const response = await api.get<Telemetry[]>(
      `${API_ENDPOINTS.telemetry.history}/${nodeId}`,
      { params: { start_time: startTime, end_time: endTime } }
    );
    return response.data;
  }

  async byCluster(clusterId: number | string): Promise<Telemetry[]> {
    const response = await api.get<Telemetry[]>(
      `${API_ENDPOINTS.telemetry.byCluster}/${clusterId}`
    );
    return response.data;
  }
}

export const telemetryService = new TelemetryService();
