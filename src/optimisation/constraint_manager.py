# Centralised hard constraints.

class ConstraintManager:
    def validate(self, optimisation):
        if not optimisation.get("feasible"):
            return False, ["Optimisation was infeasible."]

        issues = []
        weights = optimisation["post_trade"]
        if abs(sum(weights.values()) - 1) > 1e-6:
            issues.append("Weights do not sum to 100%.")
        if min(weights.values()) < -1e-8:
            issues.append("Negative weight.")
        if optimisation["turnover"] > .20 + 1e-6:
            issues.append("Turnover exceeds 20%.")
        if weights["indian_equity"] + weights["international_equity"] > .80 + 1e-6:
            issues.append("Equity concentration exceeds 80%.")
        return not issues, issues
