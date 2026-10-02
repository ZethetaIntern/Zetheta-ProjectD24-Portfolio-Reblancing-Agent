import pandas as pd
from src.optimisation.tax_optimiser import TaxOptimiser

def test_tax_estimate_nonnegative():
    portfolio = pd.Series({"tax_rate": .20})
    result = TaxOptimiser().optimise(
        portfolio,
        [{"action": "SELL", "trade_value": 100000}]
    )
    assert result["estimated_tax"] >= 0
