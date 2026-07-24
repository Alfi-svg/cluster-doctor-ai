"""
Application Enums.
"""

from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    RESEARCHER = "RESEARCHER"
    OPERATOR = "OPERATOR"


class ClusterStatus(str, Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    OFFLINE = "OFFLINE"


class NodeStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    MAINTENANCE = "MAINTENANCE"
    FAILED = "FAILED"


class ExperimentStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    STOPPED = "STOPPED"


class PredictionStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class NotificationStatus(str, Enum):
    UNREAD = "UNREAD"
    READ = "READ"


class ThreatLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"