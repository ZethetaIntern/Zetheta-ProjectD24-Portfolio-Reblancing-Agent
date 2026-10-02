import pandas as pd
from src.monitoring.drift_calculator import DriftCalculator

def test_drift_is_zero_for_target():
    row = {
        "portfolio_id": "PF-1",
        "risk_category": "Balanced",
        "indian_equity": .35,
        "international_equity": .15,
        "indian_fixed_income": .21,
        "international_fixed_income": .09,
        "alternatives": .12,
        "cash": .08,
    }
    # Missing unrelated columns are fine for calculate_one.
    result = DriftCalculator.calculate_one(pd.Series(row))
    assert result["max_drift"] < 1e-9
    assert result["breached"] is False
