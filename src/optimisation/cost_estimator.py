# Transaction-cost model.

def estimate(portfolio_value, trades, bps=12):
    # Trade value is the sum of absolute trade notionals.
    trade_value = sum(x["trade_value"] for x in trades)
    explicit = trade_value * bps / 10000
    # Simple market-impact proxy inspired by the specification.
    impact = 0.0002 * (trade_value / max(portfolio_value, 1)) ** .5 * trade_value
    return {
        "trade_value": trade_value,
        "explicit_cost": explicit,
        "market_impact_proxy": impact,
        "total_cost": explicit + impact,
        "bps": bps,
    }
