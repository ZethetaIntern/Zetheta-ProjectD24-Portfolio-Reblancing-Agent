# Convert optimiser weights into an auditable trade list.

from src.data.portfolio_generator import ASSETS

def generate(portfolio, optimisation):
    trades = []
    if not optimisation.get("feasible"):
        return trades

    for asset in ASSETS:
        delta = optimisation["post_trade"][asset] - optimisation["current"][asset]
        if abs(delta) >= 1e-5:
            trades.append({
                "asset": asset,
                "action": "BUY" if delta > 0 else "SELL",
                "weight_change": float(delta),
                "trade_value": float(abs(delta) * portfolio["portfolio_value"]),
            })
    return trades
