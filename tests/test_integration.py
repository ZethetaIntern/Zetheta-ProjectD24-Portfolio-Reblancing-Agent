import pandas as pd
from src.monitoring.drift_calculator import DriftCalculator
from src.agents.orchestrator import Orchestrator

def test_full_rebalancing_workflow():
    row = pd.Series({
        "portfolio_id": "PF-1",
        "risk_category": "Balanced",
        "portfolio_value": 1_000_000,
        "days_since_rebalance": 120,
        "tax_rate": .20,
        "liquidity_need": .05,
        "indian_equity": .55,
        "international_equity": .15,
        "indian_fixed_income": .10,
        "international_fixed_income": .04,
        "alternatives": .10,
        "cash": .06,
    })
    drift = DriftCalculator.calculate_one(row)
    result = Orchestrator().run(row, drift)
    assert result["status"] in {"MONITOR", "REBALANCE", "ESCALATE"}
