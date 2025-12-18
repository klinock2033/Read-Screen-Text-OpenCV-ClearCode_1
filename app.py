from services.ocr_stub import OCRStub
from services.text_service import TextService
from services.api_service import APIService
from core.use_cases import ReadAndSendTextUseCase
from core.runner import AppRunner
from core.logger import setup_logger
from core.config import AppConfig
from core.signal_handler import SignalHandler


class App:
    def __init__(self):
        config = AppConfig.from_env()
        # self.ocr_service = OCRService(languages='eng+rus')
        self.ocr_service = OCRStub()
        self.text_service = TextService()
        self.api = APIService(config.api_base_url)
        self.logger = setup_logger()
        self.read_and_send_text_use_case = ReadAndSendTextUseCase(
            self.ocr_service,
            self.text_service,
            self.api
        )
        self.logger.info('App wil start with config:')
        self.logger.info('Config interval: %s', config.interval)
        self.logger.info('Config base url: %s', config.api_base_url)
        self.runner = AppRunner(self.read_and_send_text_use_case, config.interval)
        self.signal_handler = SignalHandler(self.shutdown)
        self.signal_handler.register()

    def shutdown(self):
        self.runner.stop()
        self.api.close()
    def run(self):
        self.logger.info('Starting app')

        self.runner.start()