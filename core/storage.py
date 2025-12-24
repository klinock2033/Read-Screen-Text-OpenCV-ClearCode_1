import json
from pathlib import Path
from core.models import ProcessedText


class TextStorage:
    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self._items = []
        self._content_set = set()
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        if self._items:
            return

        if not self.path.exists():
            return

        with open(self.path, "r", encoding="utf-8") as f:
            for raw_line in f:
                try:
                    line = json.loads(raw_line)
                    text = ProcessedText.from_dict(line)
                    self._items.append(text)

                    self._content_set.add(text.content)

                except (json.JSONDecodeError, KeyError):
                    continue

    def save(self, text: ProcessedText) -> None:

        if self.exists(text.content):
            return

        self._items.append(text)
        self._content_set.add(text.content)

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'a', encoding="utf-8") as f:
            json.dump(text.to_dict(), f)
            f.write("\n")

    def exists(self, content: str) -> bool:
        return content in self._content_set

    def load_all(self) -> list[ProcessedText]:
        return list(self._items)
