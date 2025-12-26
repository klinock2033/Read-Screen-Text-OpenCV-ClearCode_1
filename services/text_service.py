import re
from difflib import SequenceMatcher
from core.models import ProcessedText
from core.logger import setup_logger

class TextService:
    def __init__(self, min_lenght: int = 5, similarity_threshold: float = 0.6):
        self.min_lenght = min_lenght
        self.similarity_threshold = similarity_threshold
        self._history: list[str] = []
        self.logger = setup_logger()

    def normalize(self, text: str) -> str:
        self.logger.info('Normalizing text: (%s)', text)
        text = text.strip()
        text = re.sub(r"[%^()+&\-\/!#@_|*$:№—`]", "", text)
        text = re.sub(r"\s+", " ", text)
        self.logger.info('Normalized text (%s)', text)
        return text

    def is_valid_length(self, text: str) -> bool:
        result = len(text) >= self.min_lenght
        self.logger.info('Is valid length: (%s)', result)
        return result

    def is_similar_to_history(self, text: str) -> bool:
        for old in self._history[-2:]:
            similarity = SequenceMatcher(None, text, old).ratio()
            self.logger.info('Similar to history: (%s)', similarity)
            if similarity > self.similarity_threshold:
                return True
        self.logger.info('Text is not similar to history',)
        return False

    def process(self, raw_text: str) -> ProcessedText | None:
        self.logger.info('=== Starting text processing ===')
        normalized = self.normalize(raw_text)
        if not self.is_valid_length(normalized):
            return None

        if self.is_similar_to_history(normalized):
            return None

        self._history.append(normalized)
        if len(self._history) > 10:
            self._history.pop(0)
        return ProcessedText.from_text(normalized)
