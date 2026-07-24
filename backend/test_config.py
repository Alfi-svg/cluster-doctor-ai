from app.core.config import settings

print("Project :", settings.PROJECT_NAME)
print("Version :", settings.API_VERSION)
print("Database:", settings.DATABASE_URL)
print("MQTT    :", settings.MQTT_HOST)
print("Redis   :", settings.REDIS_HOST)