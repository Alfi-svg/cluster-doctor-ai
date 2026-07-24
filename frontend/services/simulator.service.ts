import { api } from "@/lib/axios";
import { API_ENDPOINTS } from "@/constants/api";

/**
 * Publishes one fake telemetry reading through the real MQTT pipeline
 * (cluster_id=1, node_id=1 — hardcoded server-side). Useful as a
 * "Seed Demo Data" action so the AI pipeline (prediction -> healing
 * -> reality -> notification -> websocket broadcast) has something
 * to react to without wiring real hardware/MQTT.
 */
class SimulatorService {
  async publish(): Promise<unknown> {
    const response = await api.post(API_ENDPOINTS.simulator.publish);
    return response.data;
  }
}

export const simulatorService = new SimulatorService();
