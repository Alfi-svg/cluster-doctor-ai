import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { Prediction } from "@/types";

export interface PredictionCreateInput {
  cluster_id: number;
  node_id: number;
  model_name: string;
  prediction_type: string;
  confidence: number;
  risk_score: number;
  probability: number;
  predicted_label: string;
  recommendation?: string;
  explanation?: string;
}

class PredictionService {
  async create(data: PredictionCreateInput): Promise<Prediction> {
    const response = await api.post<Prediction>(API_ENDPOINTS.predictions.create, data);
    return response.data;
  }

  async get(id: number | string): Promise<Prediction> {
    const response = await api.get<Prediction>(`${API_ENDPOINTS.predictions.byId}/${id}`);
    return response.data;
  }

  async latest(nodeId: number | string): Promise<Prediction> {
    const response = await api.get<Prediction>(
      `${API_ENDPOINTS.predictions.latest}/${nodeId}`
    );
    return response.data;
  }

  async byNode(nodeId: number | string): Promise<Prediction[]> {
    const response = await api.get<Prediction[]>(
      `${API_ENDPOINTS.predictions.byNode}/${nodeId}`
    );
    return response.data;
  }

  async byModel(modelName: string): Promise<Prediction[]> {
    const response = await api.get<Prediction[]>(
      `${API_ENDPOINTS.predictions.byModel}/${modelName}`
    );
    return response.data;
  }

  async highRisk(threshold = 80): Promise<Prediction[]> {
    const response = await api.get<Prediction[]>(API_ENDPOINTS.predictions.highRisk, {
      params: { threshold },
    });
    return response.data;
  }

  async pending(): Promise<Prediction[]> {
    const response = await api.get<Prediction[]>(API_ENDPOINTS.predictions.pending);
    return response.data;
  }
}

export const predictionService = new PredictionService();
