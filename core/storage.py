import json
from pathlib import Path
from core.models import ProcessedText

class TextStorage:
    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

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
