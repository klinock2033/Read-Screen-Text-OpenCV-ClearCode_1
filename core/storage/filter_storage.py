import json
from pathlib import Path
from core.logger import setup_logger


class FilterStorage:
    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self.logger = setup_logger()

    def load_filter_file(self) -> list:
        """Load filter file from a json file"""
        if not self.path.exists():
            self.logger.error("Filter file does not exist")
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                self.logger.error("Filter file must be contain a list")
                return []
            return data
        except json.JSONDecodeError:
            self.logger.error("Filter file could not be decoded")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error to reading filters file: {e}")
            return []
