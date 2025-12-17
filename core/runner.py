import time
from core.use_cases import ReadAndSendTextUseCase

class AppRunner:
    def __init__(
            self,
    use_case: ReadAndSendTextUseCase,
    interval: float = 1.0):
        self.use_case = use_case
        self.interval = interval
        self._running = False

    def start(self):
        self._running = True
        while self._running:
            try:
                self.use_case.execute()
            except Exception as e:
                print("Runner error:", e)
            time.sleep(self.interval)

    def stop(self):
        self._running = False