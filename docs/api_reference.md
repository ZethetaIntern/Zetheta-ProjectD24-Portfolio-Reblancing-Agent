# API Reference

The most important public interfaces are:

```python
DriftCalculator.calculate_one(portfolio)
DriftCalculator.calculate_many(portfolios)

TriggerEvaluator.evaluate(portfolio, drift, event)

PortfolioOptimiser.optimise(portfolio)
TaxOptimiser.optimise(portfolio, trades)

Orchestrator.run(portfolio, drift, event)

StrategyComparator.run(scenario)
ScenarioRunner.run_all()
```

The Gradio application is launched through `python app.py`.
