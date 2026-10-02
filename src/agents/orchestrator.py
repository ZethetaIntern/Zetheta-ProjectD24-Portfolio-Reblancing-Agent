# Main multi-agent orchestrator with a bounded compliance retry loop.

from src.triggers.trigger_evaluator import TriggerEvaluator
from src.agents.portfolio_analyst import PortfolioAnalyst
from src.agents.tax_specialist import TaxSpecialist
from src.agents.risk_manager import RiskManager
from src.agents.compliance_officer import ComplianceOfficer
from src.agents.explanation_writer import ExplanationWriter
from src.optimisation.cost_estimator import estimate

class Orchestrator:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def run(self, portfolio, drift, event="None"):
        # Trigger evaluation happens before expensive optimisation.
        trigger = TriggerEvaluator().evaluate(portfolio, drift, event)

        if not trigger["triggered"]:
            return {"status": "MONITOR", "trigger": trigger}

        last = None
        for attempt in range(1, self.max_retries + 1):
            recommendation = PortfolioAnalyst().run(portfolio)
            recommendation = TaxSpecialist().run(portfolio, recommendation)
            recommendation = RiskManager().run(portfolio, recommendation)
            recommendation = ComplianceOfficer().run(recommendation)
            last = recommendation

            if recommendation["compliance"]["passed"]:
                recommendation["cost"] = estimate(
                    portfolio["portfolio_value"], recommendation["trades"]
                )
                recommendation["explanations"] = ExplanationWriter().run(
                    portfolio, drift, trigger, recommendation
                )
                recommendation["attempt"] = attempt
                return {
                    "status": "REBALANCE",
                    "trigger": trigger,
                    "recommendation": recommendation,
                }

        # Escalation is required when the automated loop cannot reach feasibility.
        return {
            "status": "ESCALATE",
            "trigger": trigger,
            "recommendation": last,
            "reason": "Compliance constraints remained unresolved after maximum retries.",
        }
