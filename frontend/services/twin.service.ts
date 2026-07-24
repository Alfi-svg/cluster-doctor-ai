import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { TwinCluster, TwinNode, TwinRoom, TwinSnapshot } from "@/types";

interface Envelope<T> {
  success: boolean;
  data: T;
}

class TwinService {
  async clusters(): Promise<TwinCluster[]> {
    const response = await api.get<Envelope<TwinCluster[]>>(API_ENDPOINTS.twin.clusters);
    return response.data.data;
  }

  async cluster(clusterId: string): Promise<TwinCluster | null> {
    const response = await api.get<Envelope<TwinCluster | Record<string, never>>>(
      `${API_ENDPOINTS.twin.clusterById}/${clusterId}`
    );
    const data = response.data.data;
    return data && "cluster_id" in data ? (data as TwinCluster) : null;
  }

  async rooms(): Promise<TwinRoom[]> {
    const response = await api.get<Envelope<TwinRoom[]>>(API_ENDPOINTS.twin.rooms);
    return response.data.data;
  }

  async node(nodeId: string): Promise<TwinNode | null> {
    const response = await api.get<Envelope<TwinNode | Record<string, never>>>(
      `${API_ENDPOINTS.twin.node}/${nodeId}`
    );
    const data = response.data.data;
    return data && "node_id" in data ? (data as TwinNode) : null;
  }

  async snapshot(nodeId: string): Promise<TwinSnapshot | null> {
    const response = await api.get<Envelope<TwinSnapshot | null>>(
      `${API_ENDPOINTS.twin.snapshot}/${nodeId}`
    );
    return response.data.data ?? null;
  }
}

export const twinService = new TwinService();
