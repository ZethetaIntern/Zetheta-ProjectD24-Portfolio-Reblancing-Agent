# Liquidity scoring and execution-risk classification.

def score(portfolio, trades):
    turnover = sum(t["trade_value"] for t in trades) / max(float(portfolio["portfolio_value"]), 1)
    need = float(portfolio["liquidity_need"])
    score = max(0, min(1, 1 - turnover - need))
    return {
        "score": score,
        "label": "HIGH" if score >= .75 else "MEDIUM" if score >= .50 else "LOW",
        "turnover": turnover,
    }
