from services.ocr_service import OCRService
from services.text_service import TextService
from services.api_service import APIService
from core.storage import TextStorage

class ReadAndSendTextUseCase:
    def __init__(self,
                 ocr: OCRService,
                 text_service: TextService,
                 api: APIService,
                 storage: TextStorage,
    ):
        self.ocr = ocr
        self.text_service = text_service
        self.api = api
        self.storage = storage

    def execute(self):
        raw_text = self.ocr.read_text()
        if not raw_text:
            return False

        processed = self.text_service.process(raw_text)
        if not processed:
            return False

        if self.storage.exists(processed):
            return False

        success: bool = self.api.send_text(processed)

        if success:
            self.storage.save(processed)

        return success