from dataclasses import dataclass
import os

@dataclass(frozen=True)
class AppConfig:
    api_base_url: str
    ocr_language: str
    interval: float
    storage_path: str

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            api_base_url=os.getenv("API_BASE_URL", "http://localhost:5000"),
            ocr_language=os.getenv("OCR_LANGUAGES", "eng+rus"),
            interval=float(os.getenv("APP_INTERVAL", "2.0")),
            storage_path=os.getenv("STORAGE_PATH", "data/history.json")
        )