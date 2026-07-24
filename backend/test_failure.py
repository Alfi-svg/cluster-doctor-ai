from app.ai.failure_prediction import FailurePredictionService

service = FailurePredictionService()

result = service.predict(
    {
        "gpu_temperature": 82,
        "fan_speed": 2400,
        "power_draw": 270,
        "cpu_utility": 88,
    }
)

print(result)