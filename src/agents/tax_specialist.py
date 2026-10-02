# Tax Specialist agent.

from src.optimisation.tax_optimiser import TaxOptimiser

class TaxSpecialist:
    def run(self, portfolio, recommendation):
        recommendation["tax"] = TaxOptimiser().optimise(
            portfolio, recommendation["trades"]
        )
        return recommendation
