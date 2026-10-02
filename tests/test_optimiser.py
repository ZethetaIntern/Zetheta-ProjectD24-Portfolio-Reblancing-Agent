import pandas as pd
from src.optimisation.portfolio_optimiser import PortfolioOptimiser

def test_optimizer_is_feasible():
    row = pd.Series({
        "risk_category": "Balanced",
        "indian_equity": .35,
        "international_equity": .15,
        "indian_fixed_income": .21,
        "international_fixed_income": .09,
        "alternatives": .12,
        "cash": .08,
    })
    result = PortfolioOptimiser().optimise(row)
    assert result["feasible"]
    assert abs(sum(result["post_trade"].values()) - 1) < 1e-6
