from src.backtesting.strategy_comparator import StrategyComparator

def test_strategy_comparison():
    df = StrategyComparator().run("normal")
    assert len(df) == 4
    assert "sharpe" in df.columns
