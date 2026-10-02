# Architecture

The project follows the PDF's separation of concerns:

- `data/` creates portfolio/client/market simulation data.
- `monitoring/` measures drift.
- `triggers/` decides whether a portfolio needs action.
- `optimisation/` generates constraint-aware trades.
- `agents/` coordinates specialist roles.
- `explainability/` creates audience-specific explanations and attribution adapters.
- `override/` handles human intervention and emergency stopping.
- `backtesting/` evaluates strategies.
- `compliance/` audits decisions.
- `dashboard/` provides application data services.
- `app.py` provides the requested Gradio UI.

Groq is intentionally outside the numerical decision path.
