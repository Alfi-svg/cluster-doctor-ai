import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { Cluster, ClusterCreateInput, ClusterUpdateInput } from "@/types";

class ClusterService {
  async list(): Promise<Cluster[]> {
    const response = await api.get<Cluster[]>(API_ENDPOINTS.clusters.list);
    return response.data;
  }

  async mine(): Promise<Cluster[]> {
    const response = await api.get<Cluster[]>(API_ENDPOINTS.clusters.mine);
    return response.data;
  }

  async get(id: number | string): Promise<Cluster> {
    const response = await api.get<Cluster>(`${API_ENDPOINTS.clusters.byId}/${id}`);
    return response.data;
  }

  async create(data: ClusterCreateInput): Promise<Cluster> {
    const response = await api.post<Cluster>(API_ENDPOINTS.clusters.create, data);
    return response.data;
  }

  async update(id: number | string, data: ClusterUpdateInput): Promise<Cluster> {
    const response = await api.put<Cluster>(`${API_ENDPOINTS.clusters.byId}/${id}`, data);
    return response.data;
  }

  async remove(id: number | string): Promise<void> {
    await api.delete(`${API_ENDPOINTS.clusters.byId}/${id}`);
  }

  async healthy(): Promise<Cluster[]> {
    const response = await api.get<Cluster[]>(API_ENDPOINTS.clusters.healthy);
    return response.data;
  }

  async critical(): Promise<Cluster[]> {
    const response = await api.get<Cluster[]>(API_ENDPOINTS.clusters.critical);
    return response.data;
  }
}

export const clusterService = new ClusterService();
