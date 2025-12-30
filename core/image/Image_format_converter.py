import cv2
import numpy as np
from PIL import Image

class ImageConverter:
    def __init__(self, logger):
        self.logger = logger

    def convert_image(self, img, current_format, target_format):
        self.logger.info(f"Converting image to {target_format}")
        match current_format , target_format:
            case "PIL", "cv2":
                img = np.array(img)
                return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            case "cv2", "PIL":
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                return Image.fromarray(img)
            case _:
                self.logger.error("Unsupported image format")
                return img


