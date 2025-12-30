from filters.filter_registry_cv2 import FilterCv2
from filters.filter_registry_pil import FilterPil

def create_filter_lib(lib_type: str, filter_list: list[dict], logger):
    libs = lib_type.split("+")
    obj = []
    for lib in libs:
        cls = FILTERS_OBJECT.get(lib)
        if cls:
            obj.append(cls(filter_list = filter_list, logger = logger))
        else:
            logger.error("Unknown filter type '%s'" % lib)
            logger.info("Adaptive ocr and filters library")
    return obj


FILTERS_OBJECT = {
    "PIL": FilterPil,
    "cv2": FilterCv2
}
