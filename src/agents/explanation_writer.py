# Explanation Writer agent delegates language generation to the Groq adapter.

from src.explainability.explanation_generator import ExplanationGenerator

class ExplanationWriter:
    def run(self, portfolio, drift, trigger, recommendation):
        generator = ExplanationGenerator()
        return {
            "client": generator.generate("client", portfolio, drift, trigger, recommendation),
            "advisor": generator.generate("advisor", portfolio, drift, trigger, recommendation),
            "compliance": generator.generate("compliance", portfolio, drift, trigger, recommendation),
        }
