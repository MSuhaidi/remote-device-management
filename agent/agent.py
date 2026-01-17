import os
import requests
import json

DEVICE_NAME = os.getenv("DEVICE_NAME")
BACKEND_URL = os.getenv("BACKEND_URL")
API_TOKEN = os.getenv("API_TOKEN")

if not all([DEVICE_NAME, BACKEND_URL, API_TOKEN]):
    print("Error: DEVICE_NAME, BACKEND_URL, and API_TOKEN environment variables must be set.")
    exit(1)

register_url = f"{BACKEND_URL}/devices/register"
headers = {
    "X-API-TOKEN": API_TOKEN,
    "Content-Type": "application/json"
}
payload = {
    "name": DEVICE_NAME
}

try:
    response = requests.post(register_url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    print("Registration successful:")
    print(json.dumps(response.json(), indent=2))
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response: {response.text}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An unexpected error occurred: {req_err}")
