from mss import mss
from PIL import Image

class MSSGrabber:
    backend = "PIL"
    def __init__(self):
        self._mss = mss()

    def grab(self, region: dict):
        img = self._mss.grab(region)
        img = Image.frombytes("RGB", img.size, img.rgb)
        return img
