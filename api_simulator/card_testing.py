import requests
import time
import argparse

"""
This script simulates a card testing / velocity attack:
Many distinct accounts send tiny amounts of money to a single merchant account
in rapid succession, mimicking fraudsters testing stolen card numbers.
"""

# Base URL of the running Flask server that handles deposits and transfers
BASE_URL = "http://localhost:5000"

# Simulate a burst of many small transfers from many different senders to one merchant
def burst(merchant, num_txns, amount):
    print(f"--- Card testing: {num_txns} txns of ${amount} to {merchant} ---")
    for i in range(num_txns):
        sender = f"cardtest_{i}"
        # seed sender with enough balance
        requests.post(f"{BASE_URL}/deposit", json={"account_id": sender, "amount": amount + 10})
        # send tiny amount to merchant
        resp = requests.post(f"{BASE_URL}/transfer", json={
            "from_account": sender,
            "to_account": merchant,
            "amount": amount
        })
        print(f"{sender} -> {merchant}: {resp.json()}")
        if i % 5 == 0:
            time.sleep(0.05)  # slight delay to avoid flooding, but still burst

# Main execution – parse arguments and run the card testing attack
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20, help="Number of tiny transfers")
    parser.add_argument("--amount", type=float, default=1.99, help="Amount per transfer")
    parser.add_argument("--merchant", type=str, default="merchant_victim")
    args = parser.parse_args()

    # ensure merchant exists (zero balance is fine)
    requests.post(f"{BASE_URL}/deposit", json={"account_id": args.merchant, "amount": 0})
    burst(args.merchant, args.count, args.amount)