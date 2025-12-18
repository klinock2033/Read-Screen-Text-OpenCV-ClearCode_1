import requests
from core.models import ProcessedText

class APIService:
    def __init__(self, base_url: str, timeout: float = 2.0):
        self.base_url = base_url
        self.timeout = timeout
        self._session = requests.Session()

    def send_text(self, text: ProcessedText) -> bool:
        try:
            response = self._session.post(
                f"{self.base_url}/read_list",
                json={"text": text.content},
                timeout=self.timeout,
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def close(self):
        self._session.close()