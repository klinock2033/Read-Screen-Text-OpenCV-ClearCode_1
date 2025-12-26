# app/bootstrap.py

from core.config import AppConfig, OCRConfig
from core.storage.factory import create_storage
from core.use_cases.read_and_send_text import ReadAndSendTextUseCase
from services.ocr_service import OCRService
from services.text_service import TextService
from services.api_service import APIService

def create_app():
    config = AppConfig.from_env()
    ocr_config = OCRConfig.from_env()

    storage = create_storage(config)

    ocr = OCRService(ocr_config)
    text_service = TextService()
    api_service = APIService(config.api_base_url)

    use_cases = ReadAndSendTextUseCase(
        ocr,
        text_service,
        api_service,
        storage
    )

    return use_cases, storage, config


