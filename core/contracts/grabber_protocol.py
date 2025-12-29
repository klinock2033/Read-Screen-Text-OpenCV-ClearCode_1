from typing import Protocol


class GrabberProtocol(Protocol):
    def grab(self, region: dict):
        pass