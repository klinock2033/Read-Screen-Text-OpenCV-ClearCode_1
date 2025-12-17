from PIL import Image
import pytesseract


class OCRService:
    def __init__(self, languages: str = 'eng'):
        self.languages = languages

    def extract_text(self, image: Image.Image) -> str:
        """Extract text from an image use OCR service"""
        return pytesseract.image_to_string(image, lang =self.languages)

    def read_text(self) -> str | None:
        """Read text from an image use OCR service"""
        raise NotImplementedError()