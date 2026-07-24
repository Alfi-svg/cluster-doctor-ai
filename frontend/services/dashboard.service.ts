import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { DashboardOverview } from "@/types";

class DashboardService {
  async overview(): Promise<DashboardOverview> {
    const response = await api.get<{ success: boolean; data: DashboardOverview }>(
      API_ENDPOINTS.dashboard.overview
    );
    return response.data.data;
  }

  async summary(): Promise<DashboardOverview> {
    const response = await api.get<{ success: boolean; summary: DashboardOverview }>(
      API_ENDPOINTS.dashboard.summary
    );
    return response.data.summary;
  }
}

export const dashboardService = new DashboardService();
