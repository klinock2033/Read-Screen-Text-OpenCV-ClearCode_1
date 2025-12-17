from services.ocr_service import OCRService
from services.text_service import TextService

class App:
    def __init__(self):
        self.ocr_service = OCRService(languages='eng+rus')
        self.text_service = TextService()

    def run(self):
        print("App running")