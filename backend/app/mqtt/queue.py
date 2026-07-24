"""
MQTT Async Queue
"""

import asyncio

# Global queue for incoming telemetry messages
telemetry_queue: asyncio.Queue = asyncio.Queue()