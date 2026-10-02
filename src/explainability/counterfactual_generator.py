# Counterfactual explanation for the threshold decision.

def generate(drift):
    # Find the minimum max-drift reduction needed to enter the configured band.
    excess = max(0.0, drift["max_drift"] - drift["band"])
    return {
        "current_max_drift": drift["max_drift"],
        "band": drift["band"],
        "required_reduction": excess,
        "statement": (
            f"If maximum drift were reduced by at least {excess:.2%}, "
            "the threshold trigger would no longer be active."
        ),
    }
