# core/use_cases/read_and_send_text.py

class ReadAndSendTextUseCase:
    def __init__(self,
                 ocr,
                 text_service,
                 api,
                 storage,
                 logger,
                 image_grab_service,
                 filter_object,
                 image_converter,

                 grabber_image_format,
                 screen_config,
                 ocr_image_format
                 ):

        self.ocr = ocr
        self.text_service = text_service
        self.api = api
        self.storage = storage
        self.logger = logger
        self.image_grab_service = image_grab_service
        self.screenshot_config = screen_config
        self.filter_object = filter_object
        self.image_converter = image_converter
        self.grabber_image_format = grabber_image_format
        self.ocr_image_format = ocr_image_format

    def execute(self):
        image_format = self.grabber_image_format
        self.logger.info("Grabbed screenshot")
        img = self.image_grab_service.grab_screen()

        if img is None:
            self.logger.error("Failed to grab screen")
            return False
        if bool(self.screenshot_config.use_filter) & bool(self.filter_object):
            self.logger.info("Try to use filter")
            for obj in self.filter_object:
                if obj.backend != image_format:
                    self.logger.info(f"Filter library image format: {obj.backend} incompatible to: {image_format}")
                    img = self.image_converter.convert_image(img=img,
                                                             current_format=self.grabber_image_format,
                                                             target_format=obj.backend)
                    image_format = obj.backend
                    img = obj.apply_image_filter(img)

        if image_format != self.ocr_image_format:
            self.logger.info(f"OCR library image format: {self.ocr_image_format} incompatible to: {image_format}")
            img = self.image_converter.convert_image(img=img,
                                                     current_format=image_format,
                                                     target_format=self.ocr_image_format)
        if img is None:
            self.logger.error("Failed to filter image")
            return False

        raw_text = self.ocr.extract_text(img)

        if not raw_text:
            self.logger.warning("No text received from OCR")
            return False

        processed = self.text_service.process(raw_text)

        if not processed:
            self.logger.warning("Can't process text")
            return False

        if self.storage.exists(processed.content):
            self.logger.warning("Can't save processed text")
            return False

        success: bool = self.api.send_text(processed)

        if success:
            self.logger.info("[][][]--> Text sent to Flask service")

        if success:
            self.logger.warning("Text successfully saved into storage")
            self.storage.save(processed)

        return success
