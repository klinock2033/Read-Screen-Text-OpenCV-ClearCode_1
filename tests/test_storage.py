import tempfile
import json
from pathlib import Path
from core.storage import TextStorage
from core.models import ProcessedText
from core.config import AppConfig
from core.use_cases import ReadAndSendTextUseCase
from services.ocr_service import OCRService
from services.ocr_stub import OCRStub
from services.text_service import TextService
from services.api_service import APIService
temp_path = None
def create_storage():
    global temp_path
    if temp_path is None:
        temp_path = Path(tempfile.mkstemp(suffix=".json")[1])

    return TextStorage(temp_path.name)


def test_save_new_text():
    storage = create_storage()
    text = ProcessedText.from_text("Hello, world!")

    assert not storage.exists(text)
    storage.save(text)
    assert storage.exists(text)

def test_duplicate_text_not_saved_twice():
    dublicate_text = 0
    config = AppConfig.from_env()
    storage = create_storage()
    ocr_service = OCRStub()
    text_service = TextService()
    api = APIService(config.api_base_url)
    usecase = ReadAndSendTextUseCase(ocr_service, text_service, api, storage)

    usecase.execute()
    usecase.execute()

    all_items = storage.load_all()
    ocr_text = ocr_service.read_text()

    for item in all_items:
        data = json.loads(item.content)
        if data["content"] == ocr_text:
            dublicate_text += 1

    assert isinstance(ocr_text, str), f"Expected OCR text to be string, got {type(ocr_text)}"
    assert dublicate_text == 1, f"Expected 1 duplicate, got {dublicate_text}"


def test_presistence_after_restart():
    storage = create_storage()
    text = ProcessedText.from_text("persistent text")

    storage.save(text)

    storage2 = TextStorage(storage.path)
    assert storage2.exists(text)