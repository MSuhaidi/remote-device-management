import os
import requests
import json
import time
import datetime
import executor

DEVICE_NAME = os.getenv("DEVICE_NAME")
BACKEND_URL = os.getenv("BACKEND_URL")
API_TOKEN = os.getenv("API_TOKEN")

if not all([DEVICE_NAME, BACKEND_URL, API_TOKEN]):
    print("Error: DEVICE_NAME, BACKEND_URL, and API_TOKEN environment variables must be set.")
    exit(1)

# --- Device Registration ---
register_url = f"{BACKEND_URL}/devices/register"
headers = {
    "X-API-TOKEN": API_TOKEN,
    "Content-Type": "application/json"
}
payload = {
    "name": DEVICE_NAME
}

registered_device_id = None
try:
    response = requests.post(register_url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    registration_data = response.json()
    registered_device_id = registration_data.get("id")
    print("Registration successful:")
    print(json.dumps(registration_data, indent=2))
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred during registration: {http_err}")
    print(f"Response: {response.text}")
    exit(1)
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred during registration: {conn_err}")
    exit(1)
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred during registration: {timeout_err}")
    exit(1)
except requests.exceptions.RequestException as req_err:
    print(f"An unexpected error occurred during registration: {req_err}")
    exit(1)

if registered_device_id is None:
    print("Error: Could not retrieve device ID from registration response.")
    exit(1)

# --- Main Loop ---
heartbeat_url = f"{BACKEND_URL}/devices/heartbeat"
job_url = f"{BACKEND_URL}/devices/{registered_device_id}/jobs/next"
heartbeat_payload = {
    "device_id": registered_device_id
}

print(f"\nStarting main loop for device ID: {registered_device_id}")
print("Press Ctrl+C to stop the agent.")

try:
    while True:
        # --- Job Polling ---
        try:
            response = requests.post(job_url, headers=headers, timeout=5)
            if response.status_code == 200:
                job_data = response.json()
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Job received: {job_data}")
                
                # Execute the script
                result = executor.run_script(job_data['script_name'])
                
                # Report the result
                report_url = f"{BACKEND_URL}/executions/{job_data['id']}/report"
                report_payload = {
                    "stdout": result['stdout'],
                    "stderr": result['stderr'],
                    "status": result['status']
                }
                report_response = requests.post(report_url, headers=headers, json=report_payload)
                report_response.raise_for_status()
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Job report submitted: {report_response.json()}")

            elif response.status_code == 204:
                # No pending jobs
                pass
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error polling for jobs: {e}")

        # --- Heartbeat ---
        time.sleep(10)
        try:
            response = requests.post(heartbeat_url, headers=headers, json=heartbeat_payload)
            response.raise_for_status()
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Heartbeat successful: {response.json()}")
        except requests.exceptions.HTTPError as http_err:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] HTTP error during heartbeat: {http_err}")
            print(f"Response: {response.text}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connection error during heartbeat: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Timeout error during heartbeat: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] An unexpected error during heartbeat: {req_err}")

except KeyboardInterrupt:
    print("\nAgent stopped by user (Ctrl+C).")
except Exception as e:
    print(f"An unhandled error occurred in the heartbeat loop: {e}")
