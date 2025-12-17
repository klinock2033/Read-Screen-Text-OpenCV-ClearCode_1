from services.ocr_stub import OCRStub
from services.text_service import TextService
from services.api_service import APIService
from core.use_cases import ReadAndSendTextUseCase
from core.runner import AppRunner


class App:
    def __init__(self):
        # self.ocr_service = OCRService(languages='eng+rus')
        self.ocr_service = OCRStub()
        self.text_service = TextService()
        self.api = APIService('http://localhost:5000')

        self.read_and_send_text_use_case = ReadAndSendTextUseCase(
            self.ocr_service,
            self.text_service,
            self.api
        )
        self.runner = AppRunner(self.read_and_send_text_use_case, interval=2.0)
    def run(self):
        print("App running")
        self.runner.start()