# Generate the 50,000-portfolio simulation universe.

from __future__ import annotations
import numpy as np
import pandas as pd

ASSETS = [
    "indian_equity",
    "international_equity",
    "indian_fixed_income",
    "international_fixed_income",
    "alternatives",
    "cash",
]

RISK = {
    "Ultra-Conservative": dict(equity=.15, fixed_income=.60, alternatives=.10, cash=.15, band=.020),
    "Conservative": dict(equity=.30, fixed_income=.45, alternatives=.12, cash=.13, band=.025),
    "Balanced": dict(equity=.50, fixed_income=.30, alternatives=.12, cash=.08, band=.030),
    "Aggressive": dict(equity=.70, fixed_income=.15, alternatives=.10, cash=.05, band=.040),
    "Ultra-Aggressive": dict(equity=.85, fixed_income=.05, alternatives=.07, cash=.03, band=.050),
}

COUNTS = {
    "Ultra-Conservative": 5000,
    "Conservative": 12000,
    "Balanced": 18000,
    "Aggressive": 10000,
    "Ultra-Aggressive": 5000,
}

def _normalise(x):
    # Force allocations to be positive and sum exactly to 1.
    x = np.clip(x, 0, None)
    return x / x.sum()

def target_vector(category):
    # Split broad equity/fixed-income targets into domestic/international components.
    r = RISK[category]
    return np.array([
        r["equity"] * .70,
        r["equity"] * .30,
        r["fixed_income"] * .70,
        r["fixed_income"] * .30,
        r["alternatives"],
        r["cash"],
    ])

def generate_portfolios(n=50000, seed=42):
    # Use equal category proportions for arbitrary n while preserving all categories.
    rng = np.random.default_rng(seed)
    categories = list(RISK)
    rows = []
    for i in range(n):
        category = categories[i % len(categories)]
        target = target_vector(category)
        current = _normalise(target + rng.normal(0, .018, len(ASSETS)))
        rows.append({
            "portfolio_id": f"PF-{i+1:05d}",
            "risk_category": category,
            "portfolio_value": float(rng.uniform(500_000, 50_000_000)),
            "days_since_rebalance": int(rng.integers(1, 181)),
            "tax_rate": float(rng.choice([.10, .20, .30])),
            "liquidity_need": float(rng.uniform(0, .20)),
            **dict(zip(ASSETS, current)),
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    # Command-line generator used by the repository setup.
    df = generate_portfolios()
    df.to_csv("data/generated/portfolios_50000.csv", index=False)
    print(f"Generated {len(df):,} portfolios.")
