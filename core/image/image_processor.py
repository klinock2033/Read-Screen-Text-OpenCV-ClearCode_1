# image_processor.py
from PIL import Image


class ImageProcessor:
    def __init__(self,
                 logger,
                 filter_registry,
                 ):
        self.logger = logger
        self.filter_registry = filter_registry

    @staticmethod
    def convert_image(img: Image) -> Image:
        return Image.frombytes("RGB", img.size, img.rgb)

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
