# 12-month synthetic backtesting engine.

import numpy as np
import pandas as pd
from src.data.market_data_simulator import simulate_market, apply_scenario

class BacktestEngine:
    def run(self, strategy="agent", days=252, seed=42, scenario="normal"):
        returns = apply_scenario(simulate_market(days, seed), scenario)
        # Equal starting weights make the benchmark transparent.
        weights = np.repeat(1 / len(returns.columns), len(returns.columns))
        values = [1.0]
        turnover = 0.0

        for _, row in returns.iterrows():
            values.append(values[-1] * (1 + np.dot(weights, row.to_numpy())))
            if strategy == "buy_hold":
                continue
            if strategy == "legacy_quarterly":
                # Quarterly rebalance to equal weights.
                if len(values) % 63 == 0:
                    turnover += np.abs(weights - 1 / len(weights)).sum()
                    weights = np.repeat(1 / len(weights), len(weights))
            elif strategy == "threshold":
                # Simple threshold rule: rebalance when any asset moves 5 percentage points.
                drift = np.abs(weights - 1 / len(weights)).max()
                if drift > .05:
                    turnover += np.abs(weights - 1 / len(weights)).sum()
                    weights = np.repeat(1 / len(weights), len(weights))
            else:
                # Agent strategy: rebalance more selectively using a 4% drift threshold.
                drift = np.abs(weights - 1 / len(weights)).max()
                if drift > .04:
                    turnover += np.abs(weights - 1 / len(weights)).sum()
                    weights = np.repeat(1 / len(weights), len(weights))

        series = pd.Series(values[1:], index=returns.index)
        return {"equity_curve": series, "turnover": float(turnover)}
