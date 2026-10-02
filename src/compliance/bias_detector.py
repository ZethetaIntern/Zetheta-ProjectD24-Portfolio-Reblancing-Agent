# Detect simple systematic differences between risk groups.

def detect(decisions):
    groups = {}
    for d in decisions:
        category = d.get("risk_category", "unknown")
        groups.setdefault(category, []).append(d.get("turnover", 0))
    return {
        k: {
            "count": len(v),
            "mean_turnover": sum(v) / len(v) if v else 0,
        }
        for k, v in groups.items()
    }
