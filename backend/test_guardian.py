from app.ai.experiment_guardian import ExperimentGuardianService

service = ExperimentGuardianService()

result = service.evaluate(
    {
        "gpu_memory_util": 82,
        "cpu_memory_util": 65,
        "allocated_cores": 16,
        "batch_size": 64,
        "epoch_progress": 45,
    }
)

print(result)