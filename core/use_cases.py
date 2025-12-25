from services.ocr_service import OCRService
from services.text_service import TextService
from services.api_service import APIService
from core.storages import TextStorage
from core.logger import setup_logger
from services.image_grab_service import ImageGrabService
from core.config import ScreenshotConfig, OCRConfig

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
        self.logger = setup_logger()
        self.image_grab_service = ImageGrabService()
        self.img_config = ScreenshotConfig.from_env()
        self.ocr_config = OCRConfig.from_env()

    def execute(self):
        img = self.image_grab_service.grab_screen(self.img_config.monitor_config)
        self.logger.info("Grabbed screenshot")
        if img is None:
            self.logger.error("Failed to grab screen")
            return False

        img = self.image_grab_service.filter_image(img)
        if img is None:
            self.logger.error("Failed to filter image")
            return False

        raw_text = self.ocr.extract_text(img, self.ocr_config.ocr_language)
        if not raw_text:
            self.logger.warning("No text received from OCR")
            return False

        processed = self.text_service.process(raw_text)
        if not processed:
            self.logger.warning("Can't process text")
            return False

        if self.storage.exists(processed.content):
            self.logger.warning("Can't save processed text")
            return False

        success: bool = self.api.send_text(processed)

        if success:
            self.logger.warning("Text successfully saved into storage")
            self.storage.save(processed)

        return success