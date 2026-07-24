import joblib

model = joblib.load("models/experiment_guardian (1).joblib")

print(type(model))

if hasattr(model, "keys"):
    print(model.keys())

print(model)