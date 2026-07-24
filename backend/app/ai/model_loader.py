from pathlib import Path
from typing import Any, Dict

import joblib


class ModelLoader:
    """
    Singleton Model Loader.

    Loads all trained models once during application startup.
    """

    _loaded = False

    _failure_predictor: Dict[str, Any] | None = None
    _anomaly_detector: Dict[str, Any] | None = None
    _experiment_guardian: Dict[str, Any] | None = None

    @classmethod
    def load_models(cls) -> None:

        if cls._loaded:
            return

        project_root = Path(__file__).resolve().parents[2]
        model_dir = project_root / "models"

        cls._failure_predictor = joblib.load(
            model_dir / "failure_predictor.joblib"
        )

        cls._anomaly_detector = joblib.load(
            model_dir / "anomaly_detector.joblib"
        )

        cls._experiment_guardian = joblib.load(
            model_dir / "experiment_guardian (1).joblib"
        )

        cls._loaded = True

        print("AI Models Loaded Successfully")

    @classmethod
    def get_failure_predictor(cls):

        if not cls._loaded:
            cls.load_models()

        return cls._failure_predictor

    @classmethod
    def get_anomaly_detector(cls):

        if not cls._loaded:
            cls.load_models()

        return cls._anomaly_detector

    @classmethod
    def get_experiment_guardian(cls):

        if not cls._loaded:
            cls.load_models()

        return cls._experiment_guardian