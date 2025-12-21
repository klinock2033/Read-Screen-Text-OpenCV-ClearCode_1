from dataclasses import dataclass
import os

@dataclass(frozen=True)
class AppConfig:
    api_base_url: str
    interval: float
    storage_path: str
    screen_save_path: str

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            api_base_url=os.getenv("API_BASE_URL", "http://localhost:5000"),
            interval=float(os.getenv("APP_INTERVAL", "2.0")),
            storage_path=os.getenv("STORAGE_PATH", "data/history.json"),
            screen_save_path=os.getenv("SCREEN_PATH", "../data/image.png")
        )
@dataclass(frozen=False)
class OCRConfig:
    ocr_language: str
    @classmethod
    def from_env(cls) -> "OCRConfig":
        return cls(
            ocr_language=os.getenv("OCR_LANGUAGES", "eng+rus"),
        )

@dataclass(frozen=False)
class ScreenshotConfig:
    monitor_config: dict
    @classmethod
    def from_env(cls) -> "ScreenshotConfig":
        return cls(
            monitor_config= os.getenv("MONITOR_CONFIG", {"top": 720, "left": 180, "width": 830, "height": 400}),
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