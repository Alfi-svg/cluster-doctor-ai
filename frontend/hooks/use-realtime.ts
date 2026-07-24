"use client";

import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { useWebSocket } from "@/hooks/use-websocket";
import { useNotificationStore } from "@/store/notification-store";
import { APP_CONFIG } from "@/constants/config";
import type { AppNotification, Prediction, ThreatLevel } from "@/types";

interface PredictionBroadcast {
  event: "prediction";
  timestamp: string;
  prediction: Partial<Prediction> & { id: number; node_id: number; cluster_id: number };
  notification: (Partial<AppNotification> & { id: number; title: string; message: string }) | null;
}

interface HeartbeatMessage {
  type: "heartbeat";
  message: string;
  echo: string;
}

type RealtimeMessage = PredictionBroadcast | HeartbeatMessage | Record<string, unknown>;

const THREAT_TOAST: Record<ThreatLevel, (msg: string, opts: { description?: string }) => void> = {
  LOW: (msg, opts) => toast.info(msg, opts),
  MEDIUM: (msg, opts) => toast.warning(msg, opts),
  HIGH: (msg, opts) => toast.warning(msg, opts),
  CRITICAL: (msg, opts) => toast.error(msg, opts),
};

/**
 * Single global subscription to the backend's only websocket route
 * (`/ws`). The server broadcasts a `{event:"prediction", prediction,
 * notification}` envelope whenever the AI pipeline finishes
 * processing a telemetry reading — this fans that out into toasts,
 * the notification bell store, and React Query cache invalidation
 * so pages refresh without polling harder than they need to.
 */
export function useRealtimeFeed(enabled = true) {
  const queryClient = useQueryClient();
  const pushNotification = useNotificationStore((s) => s.pushNotification);
  const { isConnected, subscribe } = useWebSocket(enabled ? APP_CONFIG.websocketUrl : "");

  useEffect(() => {
    if (!enabled) return;

    const unsubscribe = subscribe<RealtimeMessage>((payload) => {
      if (!payload || typeof payload !== "object") return;

      if ("event" in payload && payload.event === "prediction") {
        const msg = payload as PredictionBroadcast;

        queryClient.invalidateQueries({ queryKey: ["predictions"] });
        queryClient.invalidateQueries({ queryKey: ["dashboard"] });
        queryClient.invalidateQueries({ queryKey: ["nodes"] });

        if (msg.notification) {
          const level = (msg.notification.threat_level as ThreatLevel) ?? "LOW";
          const toastFn = THREAT_TOAST[level] ?? THREAT_TOAST.LOW;

          toastFn(msg.notification.title ?? "New AI Event", {
            description: msg.notification.message,
          });

          pushNotification({
            id: msg.notification.id,
            title: msg.notification.title ?? "AI Event",
            message: msg.notification.message ?? "",
            category: msg.notification.category ?? "prediction",
            threat_level: level,
            user_id: msg.notification.user_id ?? 0,
            cluster_id: msg.prediction.cluster_id,
            node_id: msg.prediction.node_id,
            prediction_id: msg.prediction.id,
            status: msg.notification.status ?? "UNREAD",
            read_at: null,
            created_at: msg.timestamp,
            updated_at: msg.timestamp,
          });

          queryClient.invalidateQueries({ queryKey: ["notifications"] });
        }
      }
    });

    return unsubscribe;
  }, [enabled, subscribe, queryClient, pushNotification]);

  return { isConnected };
}
