#App configs
from dataclasses import dataclass
import os, json

from services.text_service import TextService


@dataclass(frozen=True)
class AppConfig:
    grabber_type: str
    interval: float
    storage_path: str
    screen_save_path: str
    storage_type: str
    sqlite_path: str
    filter_path: str
    dialog_name: bool

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            interval=float(os.getenv("APP_INTERVAL", "2.0")),
            storage_path=os.getenv("STORAGE_PATH", "data/history.json"),
            screen_save_path=os.getenv("SCREEN_PATH", "../data/image.png"),
            sqlite_path=os.getenv("SQLITE_PATH", "data/texts.db"),
            filter_path=os.getenv("FILTER_PATH", "data/filter.json"),
            storage_type=os.getenv("STORAGE_TYPE", "json"),
            dialog_name=os.getenv("DIALOG_NAME", "false").lower() == "true",
            grabber_type=os.getenv("GRABBER_TYPE", "mss"),

        )

@dataclass(frozen=True)
class ApiUrl:
    api_base_url: str

    @classmethod
    def from_env(cls) -> "ApiUrl":
        return cls(api_base_url=os.getenv("API_BASE_URL", "http://localhost:5000"))


@dataclass(frozen=False)
class OCRConfig:
    ocr_language: str
    ocr_type: str

    @classmethod
    def from_env(cls) -> "OCRConfig":
        return cls(
            ocr_language=os.getenv("OCR_LANGUAGES", "eng+rus"),
            ocr_type=os.getenv("OCR_TYPE", "pytesseract")
        )

@dataclass(frozen=False)
class ScreenshotConfig:
    use_filter: bool
    monitor_config: dict
    monitor_config_name: dict
    @classmethod
    def from_env(cls) -> "ScreenshotConfig":
        raw = os.getenv( "MONITOR_CONFIG", '{"top": 720, "left": 180, "width": 830, "height": 400}' )
        monitor_config = json.loads(raw)
        raw = os.getenv("MONITOR_CONFIG_NAME", '{"top": 720, "left": 180, "width": 830, "height": 400}')
        monitor_config_name = json.loads(raw)
        return cls(
            monitor_config = monitor_config,
            monitor_config_name = monitor_config_name,
            use_filter = os.getenv("USE_FILTER", "false").lower() == "true"
        )


@dataclass(frozen=False)
class KeyBindingConfig:
    key_dialog: str
    key_autor: str
    @classmethod
    def from_env(cls) -> "KeyBindingConfig":
        return cls(
            key_dialog=os.getenv("KEY_DIALOG", "z"),
            key_autor=os.getenv("KEY_DIALOG", "ctrl+z")
        )