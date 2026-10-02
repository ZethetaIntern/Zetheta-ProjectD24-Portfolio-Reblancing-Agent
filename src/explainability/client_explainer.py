# Client-level explanation wrapper.

from .explanation_generator import ExplanationGenerator

def explain(portfolio, drift, trigger, recommendation):
    return ExplanationGenerator().generate("client", portfolio, drift, trigger, recommendation)
