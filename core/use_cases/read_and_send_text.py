from services.ocr_service import OCRService
from services.text_service import TextService
from services.api_service import APIService
from core.storage.base import TextStorageBase
from core.logger import setup_logger
from services.image_grab_service import ImageGrabService
from core.config import ScreenshotConfig, OCRConfig, AppConfig
from core.storage.filter_storage import FilterStorage

class ReadAndSendTextUseCase:
    def __init__(self,
                 ocr: OCRService,
                 text_service: TextService,
                 api: APIService,
                 storage: TextStorageBase,
    ):

        self.ocr = ocr
        self.text_service = text_service
        self.api = api
        self.storage = storage
        self.logger = setup_logger()
        self.image_grab_service = ImageGrabService()
        self.img_config = ScreenshotConfig.from_env()
        self.ocr_config = OCRConfig.from_env()
        self.app_config = AppConfig.from_env()

        self.filter_storage = FilterStorage(self.app_config.filter_path)
        self._use_filter: bool = self.img_config.use_filter
        self._filters_list: list = self.filter_storage.load_filter_file()
        self.logger.warning(f"Loading filter file<><><><> {self._filters_list}")


    def execute(self):
        img = self.image_grab_service.grab_screen(self.img_config.monitor_config)
        self.logger.info("Grabbed screenshot")
        if img is None:
            self.logger.error("Failed to grab screen")
            return False
        if self._use_filter:
            img = self.image_grab_service.apply_image_filter(img, self._filters_list)
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
            self.logger.info("[][][]--> Text sent to Flask service")

        if success:
            self.logger.warning("Text successfully saved into storage")
            self.storage.save(processed)

        return success