from filters.filter_registry_pil import FILTER_REGISTRY


class ImageGrabService:
    def __init__(self,
                 app_config,
                 screen_config,
                 logger,
                 grabber,
                 ):
        self.app_config = app_config
        self.screen_config = screen_config
        self.grabber = grabber
        self.filter_registry = FILTER_REGISTRY
        self.logger = logger

    def grab_screen(self):
        return self.grabber.grab(self.screen_config.monitor_config)


# show = ImageGrabService()
# show.grab_and_save()