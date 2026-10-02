# Optional SHAP adapter.
# The simulator's core decision is deterministic, so this adapter exposes a
# transparent feature-attribution interface without making SHAP a hard runtime dependency.

def explain_features(features):
    total = sum(abs(float(v)) for v in features.values()) or 1.0
    return {k: abs(float(v)) / total for k, v in features.items()}
