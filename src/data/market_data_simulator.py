# Synthetic market data replaces paid feeds for the free implementation.

from __future__ import annotations
import numpy as np
import pandas as pd
from .portfolio_generator import ASSETS

def simulate_market(days=252, seed=42):
    # Correlated daily returns for six asset classes.
    rng = np.random.default_rng(seed)
    vol = np.array([.018, .020, .006, .008, .010, .001])
    corr = np.eye(6)
    corr[0, 1] = corr[1, 0] = .55
    corr[2, 3] = corr[3, 2] = .60
    corr[0, 4] = corr[4, 0] = .20
    cov = np.outer(vol, vol) * corr
    returns = rng.multivariate_normal(np.zeros(6), cov, days)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days, freq="B")
    return pd.DataFrame(returns, index=dates, columns=ASSETS)

def apply_scenario(returns, scenario="normal"):
    # Apply deterministic stress patterns for scenario testing.
    out = returns.copy()
    if scenario == "2008_like_crash":
        out.iloc[-30:, 0:2] -= .020
        out.iloc[-30:, 2:4] -= .004
    elif scenario == "2020_like_v_recovery":
        out.iloc[-20:, 0:2] -= .025
        out.iloc[-10:, 0:2] += .040
    elif scenario == "2022_rate_shock":
        out.iloc[-40:, 2:4] -= .006
        out.iloc[-40:, 0:2] -= .008
    elif scenario == "custom_equity_credit":
        out.iloc[-35:, 0:2] -= .022
        out.iloc[-35:, 2:4] -= .007
    return out
