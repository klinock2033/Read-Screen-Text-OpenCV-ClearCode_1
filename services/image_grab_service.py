import os
import mss
from PIL import Image, ImageEnhance, ImageFilter
from core.config import AppConfig, ScreenshotConfig
from filters.filter_registry import FILTER_REGISTRY
from core.logger import setup_logger

class ImageGrabService:
    def __init__(self):
        self.mss = mss.mss()
        self.config = AppConfig.from_env()
        self.screenshot_config = ScreenshotConfig.from_env()
        self.filter_registry = FILTER_REGISTRY
        self.logger = setup_logger()

    def grab_screen(self, monitor_config: dict):
        img = self.mss.grab(monitor_config)
        img = Image.frombytes("RGB", img.size, img.rgb)
        return img

    def apply_image_filter(self, img: Image, filters: list[dict]) -> Image:
        self.logger.info("Applying image filter")
        for f in filters:
            f_type = f.get("type")
            if f_type not in self.filter_registry:
                self.logger.error("Unknown filter type: {}".format(f_type))
                continue
            try:
                img = self.filter_registry[f_type](img, **f)
            except Exception as e:
                self.logger.error(f"Error applying filter: {e}")
        return img

    def grab_and_save(self):
        os.makedirs(os.path.dirname(self.config.screen_save_path), exist_ok=True)
        img = self.grab_screen(self.screenshot_config.monitor_config)
        img.save(self.config.screen_save_path)

# show = ImageGrabService()
# show.grab_and_save()