import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RefreshTokenResponse,
  User,
} from "@/types";

class AuthService {
  async login(data: LoginRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>(
      API_ENDPOINTS.auth.login,
      data
    );

    return response.data;
  }

  async register(data: RegisterRequest): Promise<User> {
    const response = await api.post<User>(
      API_ENDPOINTS.auth.register,
      data
    );

    return response.data;
  }

  async me(): Promise<User> {
    const response = await api.get<User>(API_ENDPOINTS.auth.me);

    return response.data;
  }

  async refresh(refreshToken: string): Promise<RefreshTokenResponse> {
    const response = await api.post<RefreshTokenResponse>(
      API_ENDPOINTS.auth.refresh,
      { refresh_token: refreshToken }
    );

    return response.data;
  }

  async logout(): Promise<void> {
    try {
      await api.post(API_ENDPOINTS.auth.logout);
    } catch {
      // Stateless on the server — client-side cleanup is what matters.
    }
  }
}

export const authService = new AuthService();
