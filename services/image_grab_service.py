import os
import mss
from PIL import Image, ImageEnhance, ImageFilter
from core.config import AppConfig, ScreenshotConfig

class ImageGrabService:
    def __init__(self):
        self.mss = mss.mss()
        self.config = AppConfig.from_env()
        self.screenshot_config = ScreenshotConfig.from_env()

    def grab_screen(self, monitor_config: dict):
        return self.mss.grab(monitor_config)

    def filter_image(self, img: Image) -> Image:
        img = self.grab_screen(self.screenshot_config.monitor_config)
        img = Image.frombytes("RGB", img.size, img.rgb)
        return img

    def grab_and_save(self):
        os.makedirs(os.path.dirname(self.config.screen_save_path), exist_ok=True)
        img = self.grab_screen(self.screenshot_config.monitor_config)
        img = Image.frombytes("RGB", img.size, img.rgb)
        img.save(self.config.screen_save_path)

# show = ImageGrabService()
# show.grab_and_save()