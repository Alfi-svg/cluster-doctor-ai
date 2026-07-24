import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { ClusterNode, NodeCreateInput, NodeUpdateInput, NodeStatus } from "@/types";

class NodeService {
  async list(): Promise<ClusterNode[]> {
    const response = await api.get<ClusterNode[]>(API_ENDPOINTS.nodes.list);
    return response.data;
  }

  async get(id: number | string): Promise<ClusterNode> {
    const response = await api.get<ClusterNode>(`${API_ENDPOINTS.nodes.byId}/${id}`);
    return response.data;
  }

  async byCluster(clusterId: number | string): Promise<ClusterNode[]> {
    const response = await api.get<ClusterNode[]>(
      `${API_ENDPOINTS.nodes.byCluster}/${clusterId}`
    );
    return response.data;
  }

  async create(data: NodeCreateInput): Promise<ClusterNode> {
    const response = await api.post<ClusterNode>(API_ENDPOINTS.nodes.create, data);
    return response.data;
  }

  async update(id: number | string, data: NodeUpdateInput): Promise<ClusterNode> {
    const response = await api.put<ClusterNode>(`${API_ENDPOINTS.nodes.byId}/${id}`, data);
    return response.data;
  }

  async remove(id: number | string): Promise<void> {
    await api.delete(`${API_ENDPOINTS.nodes.byId}/${id}`);
  }

  async online(): Promise<ClusterNode[]> {
    const response = await api.get<ClusterNode[]>(API_ENDPOINTS.nodes.online);
    return response.data;
  }

  async offline(): Promise<ClusterNode[]> {
    const response = await api.get<ClusterNode[]>(API_ENDPOINTS.nodes.offline);
    return response.data;
  }

  async updateStatus(id: number | string, status: NodeStatus): Promise<ClusterNode> {
    const response = await api.patch<ClusterNode>(
      API_ENDPOINTS.nodes.status(id),
      null,
      { params: { status_value: status } }
    );
    return response.data;
  }
}

export const nodeService = new NodeService();
