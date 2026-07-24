from app.ai.model_loader import ModelLoader

ModelLoader.load_models()

failure = ModelLoader.get_failure_predictor()

print(failure.keys())