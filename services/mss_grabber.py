from mss import mss


class MSSGrabber:
    def __init__(self):
        self._mss = mss()

    def grab(self, region: dict):
        return self._mss.grab(region)