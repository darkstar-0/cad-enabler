import hashlib
import hmac
import time
import requests
from urllib.parse import urlencode

# **Onshape API Authentication**
class OnshapeClient:
    def __init__(self, base_url, access_key, secret_key):
        self.base_url = base_url
        self.access_key = access_key
        self.secret_key = secret_key

    def _generate_headers(self, method, url, query_params=None):
        # Generate the HMAC signature
        timestamp = str(int(time.time() * 1000))
        nonce = hashlib.sha256(timestamp.encode()).hexdigest()
        query_string = urlencode(query_params or {})
        full_url = f"{url}?{query_string}" if query_params else url

        # String to sign
        string_to_sign = f"{method}\n{nonce}\n{timestamp}\n{full_url}\n".lower()
        signature = hmac.new(
            self.secret_key.encode(),
            string_to_sign.encode(),
            hashlib.sha256
        ).hexdigest()

        # Headers
        headers = {
            "Authorization": f"On {self.access_key}:{signature}",
            "Date": timestamp,
            "Nonce": nonce
        }
        return headers

    def make_request(self, method, endpoint, query_params=None, body=None):
        url = f"{self.base_url}{endpoint}"
        headers = self._generate_headers(method, url, query_params)
        response = requests.request(method, url, headers=headers, params=query_params, json=body)
        return response.json()

# **Usage Example**
if __name__ == "__main__":
    # Replace with your Onshape API keys and base URL
    BASE_URL = "https://cad.onshape.com/api"
    ACCESS_KEY = "your_access_key_here"
    SECRET_KEY = "your_secret_key_here"

    client = OnshapeClient(BASE_URL, ACCESS_KEY, SECRET_KEY)

    # Example: Get account information
    endpoint = "/users/sessioninfo"
    response = client.make_request("GET", endpoint)
    print(response)
