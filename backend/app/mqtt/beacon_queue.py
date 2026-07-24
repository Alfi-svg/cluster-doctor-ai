"""
Beacon Queue

Receives ESP32 requests and forwards
them to the Beacon Worker.
"""

import asyncio

beacon_queue: asyncio.Queue = asyncio.Queue()