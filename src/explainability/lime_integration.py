# Optional LIME adapter placeholder with deterministic feature weights.

def explain_local(features):
    total = sum(abs(float(v)) for v in features.values()) or 1.0
    return sorted(
        ((k, abs(float(v)) / total) for k, v in features.items()),
        key=lambda x: x[1],
        reverse=True,
    )
