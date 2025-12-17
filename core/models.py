from dataclasses import dataclass
import time


@dataclass
class ProcessedText:
    content: str
    timestamp: str
    length: int

    @classmethod
    def from_text(cls, text: str) -> "ProcessedText":
        return cls(
            content=text,
            timestamp=time.time(),
            length=len(text)
        )