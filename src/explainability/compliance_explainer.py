# Compliance-level explanation wrapper.

from .explanation_generator import ExplanationGenerator

def explain(portfolio, drift, trigger, recommendation):
    return ExplanationGenerator().generate("compliance", portfolio, drift, trigger, recommendation)
