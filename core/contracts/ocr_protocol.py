from typing import Protocol
from PIL import Image


class OCRProtocol(Protocol):
    """OCR protocol"""
    def image_to_text(self, image: Image, lang:str) -> str:
        pass