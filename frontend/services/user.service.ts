import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { User } from "@/types";

export interface UserUpdateInput {
  full_name?: string;
  password?: string;
  is_active?: boolean;
}

class UserService {
  async updateMe(data: UserUpdateInput): Promise<User> {
    const response = await api.put<User>(API_ENDPOINTS.users.me, data);
    return response.data;
  }
}

export const userService = new UserService();
