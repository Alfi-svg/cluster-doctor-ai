"""
Application Entry Point
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import logger, setup_logging

from app.websocket.router import router as websocket_router

from app.mqtt.publisher import mqtt_publisher
from app.mqtt.subscriber import mqtt_subscriber
from app.mqtt.worker import mqtt_worker
from app.mqtt.beacon_worker import beacon_worker

# ==========================================================
# Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup & Shutdown Events
    """
    await beacon_worker.start()
    setup_logging()

    logger.info("==========================================")
    logger.info("🚀 Cluster Doctor API Starting...")
    logger.info("==========================================")

    # ------------------------------------------------------
    # Start MQTT Worker
    # ------------------------------------------------------

    await mqtt_worker.start()

    # ------------------------------------------------------
    # Start MQTT Publisher
    # ------------------------------------------------------

    mqtt_publisher.connect()

    # ------------------------------------------------------
    # Start MQTT Subscriber
    # ------------------------------------------------------

    mqtt_subscriber.connect()
    mqtt_subscriber.start()

    logger.info(f"Project : {settings.PROJECT_NAME}")
    logger.info(f"Version : {settings.API_VERSION}")
    logger.info("MQTT Worker Started")
    logger.info("MQTT Publisher Connected")
    logger.info("MQTT Subscriber Started")

    yield

    # ------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------
    await beacon_worker.stop()
    logger.info("==========================================")
    logger.info("🛑 Cluster Doctor API Stopping...")
    logger.info("==========================================")

    # Stop Subscriber
    mqtt_subscriber.stop()

    # Stop Publisher
    mqtt_publisher.disconnect()

    # Stop Worker
    await mqtt_worker.stop()

    logger.info("==========================================")
    logger.info("✅ Cluster Doctor API Stopped")
    logger.info("==========================================")


# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# API Routes
# ==========================================================

app.include_router(
    api_router,
    prefix="/api/v1",
)

app.include_router(
    websocket_router,
)


# ==========================================================
# Root
# ==========================================================

@app.get("/")
async def root():

    return {
        "project": settings.PROJECT_NAME,
        "version": settings.API_VERSION,
        "status": "running",
        "documentation": "/docs",
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "mqtt": {
            "publisher": "running",
            "subscriber": "running",
            "worker": "running",
        },
        "websocket": "running",
    }