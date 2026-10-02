# Required stress scenarios.

from .strategy_comparator import StrategyComparator

SCENARIOS = [
    "normal",
    "2008_like_crash",
    "2020_like_v_recovery",
    "2022_rate_shock",
    "custom_equity_credit",
]

class ScenarioRunner:
    def run_all(self):
        comparator = StrategyComparator()
        return {scenario: comparator.run(scenario) for scenario in SCENARIOS}
