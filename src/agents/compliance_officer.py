# Compliance Officer agent.

from src.optimisation.constraint_manager import ConstraintManager

class ComplianceOfficer:
    def run(self, recommendation):
        passed, issues = ConstraintManager().validate(recommendation["optimisation"])
        recommendation["compliance"] = {
            "passed": passed,
            "issues": issues,
            "rules": [
                "Long-only",
                "Weights sum to 100%",
                "Maximum turnover 20%",
                "Maximum equity concentration 80%",
            ],
        }
        return recommendation
