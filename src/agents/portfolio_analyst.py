# Portfolio Analyst agent.

from src.optimisation.portfolio_optimiser import PortfolioOptimiser
from src.optimisation.trade_list_generator import generate

class PortfolioAnalyst:
    def run(self, portfolio):
        optimisation = PortfolioOptimiser().optimise(portfolio)
        trades = generate(portfolio, optimisation)
        return {"optimisation": optimisation, "trades": trades}
