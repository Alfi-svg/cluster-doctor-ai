"""
Telemetry Simulator
"""

from __future__ import annotations

import random

from app.mqtt.publisher import mqtt_publisher
from app.mqtt.topics import TELEMETRY_TOPIC


class TelemetrySimulator:

    def generate(self) -> dict:

        return {

            "cluster_id": 1,
            "node_id": 1,

            "cpu_usage": random.uniform(20, 95),
            "cpu_temperature": random.uniform(35, 80),
            "cpu_frequency": 3200,

            "gpu_usage": random.uniform(10, 90),
            "gpu_temperature": random.uniform(40, 85),
            "gpu_memory_usage": random.uniform(20, 90),
            "gpu_power": random.uniform(80, 250),

            "ram_usage": random.uniform(20, 95),
            "swap_usage": random.uniform(0, 40),

            "disk_usage": random.uniform(10, 90),
            "disk_read_speed": random.uniform(50, 500),
            "disk_write_speed": random.uniform(50, 500),

            "network_in": random.uniform(10, 100),
            "network_out": random.uniform(10, 100),

            "latency": random.uniform(1, 10),
            "packet_loss": random.uniform(0, 2),
        }

    def publish(self):

        payload = self.generate()

        mqtt_publisher.publish(
            TELEMETRY_TOPIC,
            payload,
        )

        return payload


telemetry_simulator = TelemetrySimulator()