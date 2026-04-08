import requests
import json
import sys

# The address of your local FastAPI server
# If your server is running on a different port, change it here.
LOCAL_URL = "http://127.0.0.1:8000/webhook"

# This is the exact payload structure your n8n node is now configured to send
mock_payload = {
    "repository_owner": "your-github-username",
    "repository_name": "SentinelScan",
    "issue_number": "42",
    "task_description": "CRITICAL: Fix potential SQL injection in the login route. The user input is not being sanitized before the query execution."
}

def run_local_test():
    print(f"[*] Sending local test payload to {LOCAL_URL}...")
    
    try:
        response = requests.post(
            LOCAL_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(mock_payload),
            timeout=5
        )
        
        print(f"[*] Status Code: {response.status_code}")
        
        if response.status_code == 202:
            print("[+] SUCCESS: FastAPI accepted the request and moved it to BackgroundTasks.")
            print("[+] Check your FastAPI terminal for the '[WORKER]' print statements.")
        else:
            print(f"[-] FAILED: Server returned {response.status_code}")
            print(f"[-] Response text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"[!] ERROR: Could not connect to the server. Is main.py running on {LOCAL_URL}?")
        sys.exit(1)

if __name__ == "__main__":
    run_local_test()