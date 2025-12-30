from PIL import ImageEnhance, ImageFilter


class FilterPil:
    backend = "PIL"
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
        return img

def apply_grayscale(img, **kwargs):
    return img.convert("L")

def apply_contrast(img, value=1.0, **kwargs):
    return ImageEnhance.Contrast(img).enhance(value)

def apply_brightness(img, value=1.0, **kwargs):
    return ImageEnhance.Brightness(img).enhance(value)

def apply_sharpness(img, value=1.0, **kwargs):
    return ImageEnhance.Sharpness(img).enhance(value)

def apply_color(img, value=1.0, **kwargs):
    return ImageEnhance.Color(img).enhance(value)

def apply_blur(img, radius=2, **kwargs):
    return img.filter(ImageFilter.GaussianBlur(radius))

def apply_edges(img, **kwargs):
    return img.filter(ImageFilter.FIND_EDGES)

FILTER_REGISTRY = {
    "grayscale": apply_grayscale,
    "contrast": apply_contrast,
    "brightness": apply_brightness,
    "sharpness": apply_sharpness,
    "color": apply_color,
    "blur": apply_blur,
    "edges": apply_edges,
}
