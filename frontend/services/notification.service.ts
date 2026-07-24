import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { AppNotification } from "@/types";

class NotificationService {
  async get(id: number | string): Promise<AppNotification> {
    const response = await api.get<AppNotification>(
      `${API_ENDPOINTS.notifications.byId}/${id}`
    );
    return response.data;
  }

  async byUser(userId: number | string): Promise<AppNotification[]> {
    const response = await api.get<AppNotification[]>(
      `${API_ENDPOINTS.notifications.byUser}/${userId}`
    );
    return response.data;
  }

  async unreadByUser(userId: number | string): Promise<AppNotification[]> {
    const response = await api.get<AppNotification[]>(
      API_ENDPOINTS.notifications.unreadByUser(userId)
    );
    return response.data;
  }

  async critical(): Promise<AppNotification[]> {
    const response = await api.get<AppNotification[]>(API_ENDPOINTS.notifications.critical);
    return response.data;
  }

  async markRead(id: number | string): Promise<AppNotification> {
    const response = await api.patch<AppNotification>(
      API_ENDPOINTS.notifications.markRead(id)
    );
    return response.data;
  }

  async remove(id: number | string): Promise<void> {
    await api.delete(`${API_ENDPOINTS.notifications.byId}/${id}`);
  }
}

export const notificationService = new NotificationService();
