#core/use_cases/read_and_send_text.py

class ReadAndSendTextUseCase:
    def __init__(self,
                 ocr,
                 text_service,
                 api,
                 storage,
                 logger,
                 image_grab_service,
                 image_processing,

                 screen_config,
                 filter_list,
    ):

        self.ocr = ocr
        self.text_service = text_service
        self.api = api
        self.storage = storage
        self.logger = logger
        self.image_grab_service = image_grab_service
        self.screenshot_config = screen_config
        self.filter_list = filter_list
        self.image_processing = image_processing


    def execute(self):
        self.logger.info("Grabbed screenshot")
        img = self.image_grab_service.grab_screen()

        if img is None:
            self.logger.error("Failed to grab screen")
            return False
        img = self.image_processing.convert_image(img)

        if self.screenshot_config.use_filter:
            img = self.image_processing.apply_image_filter(img, self.filter_list)

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