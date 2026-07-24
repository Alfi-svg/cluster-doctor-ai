"""
MQTT Topic Definitions

All MQTT topics used across the system.
Never hardcode topic names anywhere else.
"""

from __future__ import annotations


class Topics:
    # ======================================================
    # Telemetry
    # ======================================================

    TELEMETRY = "clusterdoctor/telemetry"
    TELEMETRY_RAW = "clusterdoctor/telemetry/raw"
    TELEMETRY_PARSED = "clusterdoctor/telemetry/parsed"

    # ======================================================
    # Prediction
    # ======================================================

    PREDICTION = "clusterdoctor/prediction"
    PREDICTION_RESULT = "clusterdoctor/prediction/result"

    # ======================================================
    # AI
    # ======================================================

    AI_RECOMMENDATION = "clusterdoctor/ai/recommendation"
    AI_REPORT = "clusterdoctor/ai/report"
    AI_ALERT = "clusterdoctor/ai/alert"

    # ======================================================
    # Device
    # ======================================================

    DEVICE_REGISTER = "clusterdoctor/device/register"
    DEVICE_STATUS = "clusterdoctor/device/status"
    HEARTBEAT = "clusterdoctor/device/heartbeat"

    # ======================================================
    # Beacon
    # ======================================================

    BEACON_REQUEST = "clusterdoctor/beacon/request"
    BEACON_RESPONSE = "clusterdoctor/beacon/response"

    # ======================================================
    # Commands
    # ======================================================

    COMMAND = "clusterdoctor/device/command"
    COMMAND_ACK = "clusterdoctor/device/ack"

    # ======================================================
    # Dashboard
    # ======================================================

    DASHBOARD = "clusterdoctor/dashboard"
    DIGITAL_TWIN = "clusterdoctor/digital-twin"
        # ======================================================
    # IoT
    # ======================================================

    IOT_STATUS = "clusterdoctor/iot/status"

    IOT_COMMAND = "clusterdoctor/iot/command"

    IOT_RESPONSE = "clusterdoctor/iot/response"

    IOT_DEVICE = "clusterdoctor/iot/device"
    # ======================================================
    # Notification
    # ======================================================

    NOTIFICATION = "clusterdoctor/notification"

    # ======================================================
    # System
    # ======================================================

    HEALTH = "clusterdoctor/system/health"
    LOG = "clusterdoctor/system/log"
    ERROR = "clusterdoctor/system/error"

    # ======================================================
    # Utility
    # ======================================================

    @classmethod
    def subscribe_topics(cls) -> list[str]:
        return [
            cls.TELEMETRY,
            cls.DEVICE_REGISTER,
            cls.HEARTBEAT,
            cls.BEACON_REQUEST,
            cls.COMMAND_ACK,
        ]

    @classmethod
    def publish_topics(cls) -> list[str]:
        return [

            cls.PREDICTION,

            cls.PREDICTION_RESULT,

            cls.AI_RECOMMENDATION,

            cls.AI_ALERT,

            cls.BEACON_RESPONSE,

            cls.NOTIFICATION,

            cls.DASHBOARD,

            cls.DIGITAL_TWIN,

            cls.IOT_STATUS,

            cls.IOT_COMMAND,

        ]


# ======================================================
# Backward Compatibility Constants
# ======================================================

TELEMETRY_TOPIC = Topics.TELEMETRY
TELEMETRY_RAW_TOPIC = Topics.TELEMETRY_RAW
TELEMETRY_PARSED_TOPIC = Topics.TELEMETRY_PARSED

PREDICTION_TOPIC = Topics.PREDICTION
PREDICTION_RESULT_TOPIC = Topics.PREDICTION_RESULT

AI_RECOMMENDATION_TOPIC = Topics.AI_RECOMMENDATION
AI_REPORT_TOPIC = Topics.AI_REPORT
AI_ALERT_TOPIC = Topics.AI_ALERT

DEVICE_REGISTER_TOPIC = Topics.DEVICE_REGISTER
DEVICE_STATUS_TOPIC = Topics.DEVICE_STATUS
HEARTBEAT_TOPIC = Topics.HEARTBEAT

BEACON_REQUEST_TOPIC = Topics.BEACON_REQUEST
BEACON_RESPONSE_TOPIC = Topics.BEACON_RESPONSE

COMMAND_TOPIC = Topics.COMMAND
COMMAND_ACK_TOPIC = Topics.COMMAND_ACK

DASHBOARD_TOPIC = Topics.DASHBOARD
DIGITAL_TWIN_TOPIC = Topics.DIGITAL_TWIN

NOTIFICATION_TOPIC = Topics.NOTIFICATION

HEALTH_TOPIC = Topics.HEALTH
LOG_TOPIC = Topics.LOG
ERROR_TOPIC = Topics.ERROR
IOT_STATUS_TOPIC = Topics.IOT_STATUS

IOT_COMMAND_TOPIC = Topics.IOT_COMMAND

IOT_RESPONSE_TOPIC = Topics.IOT_RESPONSE

IOT_DEVICE_TOPIC = Topics.IOT_DEVICE
# ======================================================
# Legacy Compatibility
# ======================================================

BEACON_TOPIC = Topics.BEACON_REQUEST