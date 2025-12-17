import re
from difflib import SequenceMatcher
from typing import Optional
from core.models import ProcessedText

class TextService:
    def __init__(self, min_lenght: int = 5, similarity_threshold: float = 0.6):
        self.min_lenght = min_lenght
        self.similarity_threshold = similarity_threshold
        self._history: list[str] = []

    def normalize(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r"[%^()+&\-\/!#@_|*$:№—`]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def is_valid_length(self, text: str) -> bool:
        return len(text) >= self.min_lenght

    def is_similar_to_history(self, text: str) -> bool:
        for old in self._history[-2:]:
            similarity = SequenceMatcher(None, text, old).ratio()
            if similarity > self.similarity_threshold:
                return True
        return False

    def process(self, raw_text: str) -> ProcessedText | None:
        normalized = self.normalize(raw_text)
        if not self.is_valid_length(normalized):
            return None

        if self.is_similar_to_history(normalized):
            return None

        self._history.append(normalized)
        if len(self._history) > 10:
            self._history.pop(0)

        return ProcessedText.from_text(normalized)
