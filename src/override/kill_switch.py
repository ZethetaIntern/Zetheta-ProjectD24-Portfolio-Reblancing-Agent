# Emergency kill switch.

class KillSwitch:
    def __init__(self):
        self.enabled = False

    def activate(self):
        self.enabled = True
        return self.enabled

    def deactivate(self):
        self.enabled = False
        return self.enabled

    def check(self):
        return self.enabled
