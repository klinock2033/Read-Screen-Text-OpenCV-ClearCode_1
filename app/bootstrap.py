# app/bootstrap.py
import mss
from core.config import AppConfig, OCRConfig, ScreenshotConfig, ApiUrl
from core.storage.factory import create_storage
from core.use_cases.read_and_send_text import ReadAndSendTextUseCase
from services.image_grab_service import ImageGrabService
from services.ocr_service import OCRService
from services.text_service import TextService
from services.api_service import APIService
from core.logger import setup_logger
from core.factories.grabber_factory import create_grabber
from core.factories.ocr_factory import create_ocr
from core.image.Image_format_converter import ImageConverter
from core.image.filter_lib_factory import create_filter_lib

import requests
from core.models import ProcessedText

def create_app():
    app_config = AppConfig.from_env()
    api_config = ApiUrl.from_env()
    ocr_config = OCRConfig.from_env()
    screen_config = ScreenshotConfig.from_env()

    ocr = create_ocr(ocr_config.ocr_type)
    process_text = ProcessedText
    storage = create_storage(app_config)
    logger = setup_logger()
    ocr_service = OCRService(ocr_config, ocr)
    text_service = TextService()
    grabber = create_grabber(app_config.grabber_type)

    image_converter = ImageConverter(logger=logger)
    filter_library = create_filter_lib(screen_config.filter_lib, [], logger)
    api_service = APIService(
        timeout= app_config.interval,
        api_url= api_config,
        requests=requests,
        process_text= process_text
    )

    image_grab_service = ImageGrabService(
        app_config= app_config,
        screen_config= screen_config,
        logger= logger,
        grabber= grabber
    )

    use_cases = ReadAndSendTextUseCase(
        ocr= ocr_service,
        ocr_image_format= ocr.backend,
        text_service= text_service,
        api= api_service,
        storage= storage,
        logger= logger,
        image_grab_service= image_grab_service,
        screen_config= screen_config,
        filter_object= filter_library,
        image_converter= image_converter,
        grabber_image_format = grabber.backend

    )

    return use_cases, storage, app_config


