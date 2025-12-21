import json
from pathlib import Path
from core.models import ProcessedText
import os

class TextStorage:
    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self._items = []
        self._content_set = set()
        self.logger.info("Initializing TextStorage")
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                data = f.readlines()
                if data:
                    for line in data:
                        try:
                            line = json.loads(line)

                            self._items.append( ProcessedText(
                                content=line["content"],
                                timestamp=line.get("timestamp", 0),
                                length=line.get("length", len(line["content"]))
                            ))

                            self._content_set.add(line["content"])

                        except json.decoder.JSONDecodeError:
                            continue

    def test(self):
        return self._items

    def load_all(self):
        items = []
        with open(self.path, 'r', encoding="utf-8") as f:
            for line in f:
                items.append(ProcessedText.from_text(line))
        return items

    def save(self, text: ProcessedText):
        with self.path.open('a', encoding='utf-8') as f:
            f.write(json.dumps({
                'content': text.content,
            },
            ensure_ascii=False,))
            f.write('\n')

    def exists(self, text: ProcessedText) -> bool:
        if not self.path.exists():
            return False

        with self.path.open('r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get('content') == text.content:
                        return True
                except json.JSONDecodeError:
                    continue
        return False

start = TextStorage
allS = start.test
