# Explicit threshold trigger adapter.

def evaluate(drift):
    return bool(drift["max_drift"] > drift["band"])
