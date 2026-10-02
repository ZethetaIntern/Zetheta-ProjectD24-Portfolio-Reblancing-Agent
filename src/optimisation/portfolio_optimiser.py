# CVXPY constrained portfolio optimisation.

import numpy as np
import cvxpy as cp
from src.data.portfolio_generator import ASSETS, target_vector

class PortfolioOptimiser:
    def optimise(self, portfolio, max_turnover=.20):
        current = portfolio[ASSETS].to_numpy(dtype=float)
        target = target_vector(portfolio["risk_category"])
        x = cp.Variable(len(ASSETS))

        # Minimise distance to strategic allocation plus turnover penalty.
        objective = cp.Minimize(cp.sum_squares(x - target) + .01 * cp.norm1(x - current))
        constraints = [
            x >= 0,
            cp.sum(x) == 1,
            cp.norm1(x - current) <= max_turnover,
            x[0] + x[1] <= .80,
        ]
        problem = cp.Problem(objective, constraints)
        problem.solve(solver=cp.CLARABEL, verbose=False)

        if x.value is None:
            # Infeasible problems are returned explicitly for escalation.
            return {"feasible": False, "reason": "No feasible solution."}

        post = np.asarray(x.value).reshape(-1)
        return {
            "feasible": True,
            "current": dict(zip(ASSETS, current)),
            "target": dict(zip(ASSETS, target)),
            "post_trade": dict(zip(ASSETS, post)),
            "turnover": float(np.abs(post - current).sum()),
        }
