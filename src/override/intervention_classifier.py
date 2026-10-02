# Classify a human intervention.

def classify(action):
    mapping = {
        "Approve": "APPROVAL",
        "Reject": "REJECTION",
        "Modify": "MODIFICATION",
        "Hold": "HOLD",
    }
    return mapping.get(action, "UNKNOWN")
