import { useCallback, useEffect, useState } from "react";

import { websocketClient } from "@/lib/websocket";

/** Pass an empty string to keep the hook mounted without opening a socket. */
export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);

  const [lastMessage, setLastMessage] = useState<unknown>(null);

  useEffect(() => {
    if (!url) return;

    const handleOpen = () => {
      setIsConnected(true);
    };

    const handleClose = () => {
      setIsConnected(false);
    };

    const handleMessage = (payload?: unknown) => {
      setLastMessage(payload);
    };

    websocketClient.on("open", handleOpen);
    websocketClient.on("close", handleClose);
    websocketClient.on("message", handleMessage);

    websocketClient.connect(url);

    return () => {
      websocketClient.off("open", handleOpen);
      websocketClient.off("close", handleClose);
      websocketClient.off("message", handleMessage);

      websocketClient.disconnect();
    };
  }, [url]);

  const connect = useCallback(() => {
    websocketClient.connect(url);
  }, [url]);

  const disconnect = useCallback(() => {
    websocketClient.disconnect();
  }, []);

  const send = useCallback((data: unknown) => {
    websocketClient.send(data);
  }, []);

  const subscribe = useCallback(
    <T = unknown>(
      callback: (payload: T) => void
    ) => {
      const handler = (payload?: unknown) => {
        callback(payload as T);
      };

      websocketClient.on("message", handler);

      return () => {
        websocketClient.off("message", handler);
      };
    },
    []
  );

  return {
    isConnected,
    lastMessage,

    connect,
    disconnect,
    send,
    subscribe,
  };
}