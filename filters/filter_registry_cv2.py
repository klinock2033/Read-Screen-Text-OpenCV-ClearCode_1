import cv2

class FilterCv2:
    backend = "cv2"
    def __init__(self, filter_list: list[dict], logger):
        self.filter_list = filter_list
        self.filter_registry = FILTER_REGISTRY
        self.logger = logger

    def apply_image_filter(self, img):
        self.logger.info("Applying image filter")

        for f in self.filter_list:
            f_type = f.get("type")

            if f_type not in self.filter_registry:
                self.logger.error("Unknown filter type: {}".format(f_type))
                continue

            try:
                img = self.filter_registry[f_type](img, **f)
            except Exception as e:
                self.logger.error(f"Error applying filter: {e}")
        img.show()
        return img


def apply_grayscale(img, **kwargs):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def apply_blur(img, ksize_a, ksize_b, sigma, **kwargs):
    return cv2.GaussianBlur(img, (ksize_a, ksize_b), sigma)

def apply_morph(img, ksize_a, ksize_b, iteration, **kwargs):

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize_a, ksize_b))
    dilated = cv2.dilate(img, kernel, iterations=iteration)
    return dilated

FILTER_REGISTRY = {
    "grayscale": apply_grayscale,
    "morph": apply_morph,
    "blur": apply_blur,
}
