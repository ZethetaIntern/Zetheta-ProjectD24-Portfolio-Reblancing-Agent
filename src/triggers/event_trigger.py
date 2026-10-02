# Explicit event trigger adapter.

def evaluate(event):
    return event not in (None, "", "None")
