#grabber_factory.py

from core.storage.base import TextStorageBase
from core.storage.json_storages import TextStorage
from core.storage.sqlite_storage import SQLiteTextStorage
from core.config import AppConfig

def create_storage(config: AppConfig) -> TextStorageBase:
    if config.storage_type == "sqlite":
        return SQLiteTextStorage(config.sqlite_path)

    if config.storage_type == "json":
        return TextStorage(config.storage_path)

    raise ValueError(f"Unknown storage type: {config.storage_type}")