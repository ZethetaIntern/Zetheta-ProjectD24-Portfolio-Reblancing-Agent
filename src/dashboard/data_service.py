# Data service used by the Gradio dashboard.

from src.data.portfolio_generator import generate_portfolios
from src.monitoring.drift_monitor import DriftMonitor

class DataService:
    def __init__(self):
        self.portfolios = generate_portfolios(50000)
        self.monitor = DriftMonitor()

    def overview(self):
        return self.monitor.scan(self.portfolios)

    def get(self, portfolio_id):
        row = self.portfolios[self.portfolios["portfolio_id"] == portfolio_id]
        if row.empty:
            return None
        return row.iloc[0]
