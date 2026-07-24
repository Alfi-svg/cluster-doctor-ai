import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";
import type { ChatAnswer, ChatRequestPayload } from "@/types";

class ChatbotService {
  async send(payload: ChatRequestPayload): Promise<ChatAnswer> {
    const response = await api.post<{
      success: boolean;
      message: string;
      data: ChatAnswer;
    }>(API_ENDPOINTS.chatbot.chat, payload);

    return response.data.data;
  }
}

export const chatbotService = new ChatbotService();
