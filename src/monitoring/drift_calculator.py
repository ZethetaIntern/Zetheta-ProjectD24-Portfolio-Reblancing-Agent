# Vectorised drift calculations for large portfolio universes.

import numpy as np
import pandas as pd
from src.data.portfolio_generator import ASSETS, RISK, target_vector

class DriftCalculator:
    @staticmethod
    def calculate_one(portfolio):
        # Calculate drift metrics for a single portfolio.
        current = portfolio[ASSETS].to_numpy(dtype=float)
        target = target_vector(portfolio["risk_category"])
        drift = current - target
        sad = float(np.abs(drift).sum())
        rmsd = float(np.sqrt(np.mean(drift ** 2)))
        band = RISK[portfolio["risk_category"]]["band"]
        # Tracking error proxy using a simple diagonal covariance matrix.
        cov = np.diag(np.array([.018, .020, .006, .008, .010, .001]) ** 2)
        tracking_error = float(np.sqrt(max(drift @ cov @ drift, 0)))
        return {
            "sad": sad,
            "rmsd": rmsd,
            "max_drift": float(np.abs(drift).max()),
            "tracking_error": tracking_error,
            "band": band,
            "breached": bool(np.abs(drift).max() > band),
            **{f"{a}_drift": float(d) for a, d in zip(ASSETS, drift)},
        }

    @staticmethod
    def calculate_many(df):
        # Vectorised implementation: avoids a Python loop over 50,000 portfolios.
        targets = np.vstack([target_vector(x) for x in df["risk_category"]])
        current = df[ASSETS].to_numpy(dtype=float)
        drift = current - targets
        abs_drift = np.abs(drift)
        result = pd.DataFrame(index=df.index)
        result["sad"] = abs_drift.sum(axis=1)
        result["rmsd"] = np.sqrt((drift ** 2).mean(axis=1))
        result["max_drift"] = abs_drift.max(axis=1)
        vol = np.array([.018, .020, .006, .008, .010, .001])
        result["tracking_error"] = np.sqrt((drift ** 2 * vol**2).sum(axis=1))
        result["band"] = df["risk_category"].map({k: v["band"] for k, v in RISK.items()})
        result["breached"] = result["max_drift"] > result["band"]
        return pd.concat([df[["portfolio_id", "risk_category"]].reset_index(drop=True),
                          result.reset_index(drop=True)], axis=1)
