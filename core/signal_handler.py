import signal
from core.logger import setup_logger

class SignalHandler:
    def __init__(self, on_shutdown):
        self.logger = setup_logger()
        self.on_shutdown = on_shutdown

    def register(self):
        signal.signal(signal.SIGINT, self._handle)
        signal.signal(signal.SIGTERM, self._handle)

    def _handle(self, signum, frame):
        self.logger.info('Shutdown signal received(%s)', signum)
        self.on_shutdown()



