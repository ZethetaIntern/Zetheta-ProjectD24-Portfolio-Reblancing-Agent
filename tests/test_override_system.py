from src.override.kill_switch import KillSwitch
from src.override.override_capture import OverrideCapture

def test_kill_switch():
    ks = KillSwitch()
    assert not ks.check()
    ks.activate()
    assert ks.check()
    ks.deactivate()
    assert not ks.check()

def test_override_capture():
    record = OverrideCapture().capture("PF-1", "Hold", "Review")
    assert record["portfolio_id"] == "PF-1"
