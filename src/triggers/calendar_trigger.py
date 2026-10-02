# Explicit calendar trigger adapter.

def evaluate(days_since_rebalance, threshold=90):
    return int(days_since_rebalance) >= threshold
