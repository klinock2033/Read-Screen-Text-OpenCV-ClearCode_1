from PIL import Image
import pytesseract


class OCRService:
    def __init__(self, config):
        self.config = config


    def extract_text(self, image: Image.Image, language: str) -> str:
        """Extract text from an image use OCR service"""
        return pytesseract.image_to_string(image, lang =language)

    def read_text(self) -> str | None:
        """Read text from an image use OCR service"""
        raise NotImplementedError()