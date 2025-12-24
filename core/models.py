from dataclasses import dataclass
import time
import json

@dataclass
class ProcessedText:
    content: str
    timestamp: float
    length: int

    @classmethod
    def from_text(cls, text: str) -> "ProcessedText":
        return cls(
            content=text,
            timestamp=time.time(),
            length=len(text)
        )
    def to_json(self) -> str:
        return json.dumps({
            "content": self.content,
            "timestamp": self.timestamp,
            "length": self.length
        }, ensure_ascii=False)

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "timestamp": self.timestamp,
            "length": self.length
        }
    @classmethod
    def from_dict(cls, data: dict) -> "ProcessedText":
        return cls(
            content=data["content"],
            timestamp=data.get("timestamp", 0),
            length=data.get("length", len(data["content"])),
        )