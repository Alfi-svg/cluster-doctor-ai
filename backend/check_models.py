from joblib import load

bundle = load("models/failure_predictor.joblib")

print("========== FEATURE LIST ==========")

for i, feature in enumerate(bundle["features"], 1):
    print(f"{i}. {feature}")