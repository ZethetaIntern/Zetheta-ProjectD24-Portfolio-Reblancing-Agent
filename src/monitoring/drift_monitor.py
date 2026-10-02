# Portfolio monitoring service.

from .drift_calculator import DriftCalculator

class DriftMonitor:
    def scan(self, portfolios):
        # Return portfolios sorted by the most severe drift.
        result = DriftCalculator.calculate_many(portfolios)
        return result.sort_values(["breached", "max_drift"], ascending=[False, False])
