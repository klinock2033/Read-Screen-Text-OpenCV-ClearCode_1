from typing import Protocol


class GrabberProtocol(Protocol):
    backend:str
    def grab(self, region: dict):
        pass