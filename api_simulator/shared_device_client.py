import requests
import time
import argparse

"""
This script simulates a fraud ring where multiple accounts all use the same X-Device-Id header
(implying they're controlled by the same attacker) and each sends money to a common "master_account".
"""

# Base URL of the running Flask server
BASE_URL = "http://localhost:5000"

# Simulate a single account using a shared device identifier (header)
def act(account, header_name, device_id, amount=50):
    headers = {header_name: device_id}
    requests.post(f"{BASE_URL}/deposit", json={"account_id": account, "amount": 200}, headers=headers)
    time.sleep(0.1)
    requests.post(f"{BASE_URL}/transfer", json={
        "from_account": account,
        "to_account": "master_account",
        "amount": amount
    }, headers=headers)
    print(f"{account} used {header_name}: {device_id}")

# Main execution – parse arguments and create a fraud ring
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--accounts", type=int, default=5)
    parser.add_argument("--device", type=str, default="compromised_device_42")
    parser.add_argument("--header", type=str, default="X-Device-Id", help="Custom header name for device fingerprint")
    args = parser.parse_args()

    # Ensure master_account exists (zero balance is fine)
    requests.post(f"{BASE_URL}/deposit", json={"account_id": "master_account", "amount": 0})

    for i in range(args.accounts):
        acc = f"ring_{i}"
        act(acc, args.header, args.device)
        time.sleep(0.1)