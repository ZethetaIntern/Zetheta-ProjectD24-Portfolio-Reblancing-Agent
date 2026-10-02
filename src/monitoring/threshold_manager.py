# Threshold management keeps trigger policy separate from calculations.

from src.data.portfolio_generator import RISK

class ThresholdManager:
    def band(self, risk_category):
        return RISK[risk_category]["band"]

    def breached(self, risk_category, max_drift):
        return float(max_drift) > self.band(risk_category)
