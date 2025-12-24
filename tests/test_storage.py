from pathlib import Path
from core.storage import TextStorage
from core.models import ProcessedText



def create_storage(name: str):
    path = Path(name)
    if path.exists(): path.unlink()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    return TextStorage(name)


def test_save_new_text():
    storage = create_storage("test_new_text.json")
    text = ProcessedText.from_text("Test save new text")

    assert not storage.exists(text.content)
    storage.save(text)
    assert storage.exists(text.content)
    if storage.path.exists(): storage.path.unlink()


def test_duplicate_not_saved_twice():
    storage = create_storage("test_duplicate_text.json")
    test_text = ProcessedText.from_text("Test duplicate history save")
    storage.save(test_text)
    storage.save(test_text)
    all_items = storage.load_all()

    assert len(all_items) == 1
    if storage.path.exists(): storage.path.unlink()


def test_presistence_after_restart():
    storage = create_storage("test_presistence_after_restart.json")
    text = ProcessedText.from_text("persistent text")

    storage.save(text)

    storage2 = TextStorage(storage.path)
    assert storage2.exists(text.content)
    if storage.path.exists(): storage.path.unlink()
