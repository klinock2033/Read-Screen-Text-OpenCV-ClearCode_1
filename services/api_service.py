#services/api_service.py

class APIService:
    def __init__(self,
                 timeout,
                 process_text,
                 api_url,
                 requests
                 ):
        self.api_url = api_url
        self.timeout = timeout
        self._session = requests.Session()
        self.process_text = process_text
        self.request_method = requests

    def send_text(self, text) -> bool:
        try:
            response = self._session.post(
                f"{self.api_url.api_base_url}/read_list",
                json={"text": text.content},
                timeout=self.timeout,
            )
            return response.status_code == 200
        except self.request_method.RequestException:
            return False

    def close(self):
        self._session.close()