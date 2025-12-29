from core.contracts.ocr_protocol import OCRProtocol
from services.pytesseract_ocr import PytesseractService

def create_ocr(ocr_type: str) -> OCRProtocol:
    if ocr_type == 'pytesseract':
        return PytesseractService()

    raise ValueError('Unknown OCR type')
