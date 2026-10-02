# Compare agent, legacy, threshold and buy-and-hold strategies.

import pandas as pd
from .backtest_engine import BacktestEngine
from .performance_analyser import PerformanceAnalyser

class StrategyComparator:
    def run(self, scenario="normal"):
        engine = BacktestEngine()
        analyser = PerformanceAnalyser()
        rows = []
        for strategy in ["agent", "legacy_quarterly", "threshold", "buy_hold"]:
            result = engine.run(strategy=strategy, scenario=scenario)
            metrics = analyser.analyse(result["equity_curve"], result["turnover"])
            rows.append({"strategy": strategy, **metrics})
        return pd.DataFrame(rows)
