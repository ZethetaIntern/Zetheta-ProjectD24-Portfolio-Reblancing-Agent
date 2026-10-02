# Performance metrics for strategy comparison.

import numpy as np

class PerformanceAnalyser:
    def analyse(self, equity_curve, turnover=0):
        returns = equity_curve.pct_change().dropna()
        annual_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (252 / len(returns)) - 1
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility else 0
        drawdown = equity_curve / equity_curve.cummax() - 1
        max_drawdown = drawdown.min()
        return {
            "annualised_return": float(annual_return),
            "volatility": float(volatility),
            "sharpe": float(sharpe),
            "max_drawdown": float(max_drawdown),
            "tracking_error": float(volatility),
            "turnover": float(turnover),
            "transaction_cost": float(turnover * .0012),
            "tax_efficiency": float(max(0, 1 - turnover * .25)),
        }
