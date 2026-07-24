from app.ai.gateway import AIGateway

gateway = AIGateway()

print("========== FAILURE ==========")

print(
    gateway.predict_failure(
        {
            "gpu_temperature": 80,
            "fan_speed": 2400,
            "power_draw": 260,
            "cpu_utility": 85,
        }
    )
)

print()

print("========== SECURITY ==========")

print(
    gateway.detect_anomaly(
        {
            "dur": 1.5,
            "spkts": 20,
            "dpkts": 21,
            "sbytes": 2000,
            "dbytes": 1800,
            "rate": 60,
            "sttl": 64,
            "dttl": 64,
            "sload": 210,
            "dload": 180,
            "tcprtt": 0.05,
            "synack": 0.02,
            "ackdat": 0.03,
        }
    )
)

print()

print("========== EXPERIMENT ==========")

print(
    gateway.evaluate_experiment(
        {
            "gpu_memory_util": 75,
            "cpu_memory_util": 60,
            "allocated_cores": 16,
            "batch_size": 64,
            "epoch_progress": 40,
        }
    )
)