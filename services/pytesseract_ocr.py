import pytesseract
from PIL import Image, ImageEnhance

class PytesseractService:
    backend = "PIL"
    def __init__(self):
        self.pytesseract = pytesseract

    def image_to_text(self, image, lang: str) -> str:
        """Extract text from an image use OCR service"""
        return self.pytesseract.image_to_string(image, lang=lang)