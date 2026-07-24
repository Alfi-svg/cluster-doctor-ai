from app.ai.feature_mapper import FeatureMapper

telemetry = {

    "cpu_usage": 82,
    "gpu_temperature": 71,
    "gpu_memory_usage": 64,
    "gpu_power": 245,

    "ram_usage": 58,

    "network_in": 3200,
    "network_out": 2800,

    "latency": 4,
}

print(FeatureMapper.failure_features(telemetry))

print()

print(FeatureMapper.guardian_features(telemetry))

print()

print(FeatureMapper.security_features(telemetry))