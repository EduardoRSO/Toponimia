import requests
import time
from datetime import datetime
from logging_logic.logging_handler import LoggingHandler

class RequestingHandler(LoggingHandler):
    def __init__(self):
        super().__init__()
        self.set_method_mapping()

    @LoggingHandler.log_method('RequestingHandler', 'set_method_mapping', show_output=False)
    def set_method_mapping(self):
        self.method_mapping = {
            'GET': requests.get,
            'POST': requests.post
        }

    def _request_wrapper(self, method_function, url, request_info, **kwargs):
        try:
            start_time = time.time()
            response = method_function(url, **kwargs)
            end_time = time.time()
            request_info["response_time"] = end_time - start_time
            request_info["response_length"] = len(response.content)
            request_info["response_string"] = response.text
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            request_info["error"] = str(e)
        return request_info

    @LoggingHandler.log_method('RequestingHandler', 'make_request', show_output=False)
    def make_request(self, method, url, **kwargs):
        if method.upper() not in self.method_mapping:
            raise ValueError(f"Method {method} not supported. Use 'GET' or 'POST'.")
        request_info = {
            "url": url,
            "method": method.upper(),
            "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "response_time": None,
            "response_length": None,
            "response_string": None,
            "error": None
        }
        return self._request_wrapper(self.method_mapping[method.upper()], url, request_info, **kwargs)
