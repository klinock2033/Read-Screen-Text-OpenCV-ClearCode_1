#base.py

from core.models import ProcessedText
from abc import ABC, abstractmethod



class TextStorageBase(ABC):


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def exists(self, content: str) -> bool:
        pass

    @abstractmethod
    def save(self, processed: ProcessedText) -> None:
        pass

    @abstractmethod
    def load_all(self) -> list[ProcessedText]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass