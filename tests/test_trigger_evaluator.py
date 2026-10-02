from src.triggers.trigger_evaluator import TriggerEvaluator

def test_threshold_trigger():
    p = {"days_since_rebalance": 10}
    drift = {"max_drift": .08, "band": .03}
    result = TriggerEvaluator().evaluate(p, drift)
    assert result["triggered"]
    assert result["type"] == "THRESHOLD"

def test_event_has_priority():
    p = {"days_since_rebalance": 1}
    drift = {"max_drift": .01, "band": .03}
    result = TriggerEvaluator().evaluate(p, drift, "Market Crash")
    assert result["type"] == "EVENT"
