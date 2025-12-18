import time
from core.use_cases import ReadAndSendTextUseCase
from core.logger import setup_logger


class AppRunner:
    def __init__(
            self,
    use_case: ReadAndSendTextUseCase,
    interval: float = 1.0):
        self.use_case = use_case
        self.interval = interval
        self._running = False
        self.logger = setup_logger()

    def start(self):
        self.logger.info("Runner started")
        self._running = True
        while self._running:
            try:
                result = self.use_case.execute()
                self.logger.info('Use case execute result: %s', result)
            except Exception as e:
                self.logger.exception('runner error: %s', e)
            time.sleep(self.interval)

    def stop(self):
        self.logger.info("Runner stopping")
        self._running = False