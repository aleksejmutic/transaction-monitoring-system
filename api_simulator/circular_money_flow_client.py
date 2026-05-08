import requests
import time
import argparse

"""
This script simulates a circular money flow (money laundering layering),
where a series of accounts send money in a loop (A → B → C → ... → A)
to obscure the original source of funds.
"""

# Base URL of the running Flask server that handles deposits and transfers
BASE_URL = "http://localhost:5000"

# Seed an account with an initial balance so it can later send money
def seed_account(account_id, initial_balance=1000):
    """
    Give an initial balance to an account by calling the /deposit endpoint.
    This ensures the account has enough funds to participate in transfers.
    """
    requests.post(f"{BASE_URL}/deposit", json={"account_id": account_id, "amount": initial_balance})

# Execute a circular money flow – each account sends money to the next, forming a cycle
def run_cycle(cycle_accounts, transfer_amount):
    print(f"--- Circular flow: {' → '.join(cycle_accounts)} → {cycle_accounts[0]} ---")
    for i in range(len(cycle_accounts)):
        sender = cycle_accounts[i]
        receiver = cycle_accounts[(i+1) % len(cycle_accounts)]
        response = requests.post(f"{BASE_URL}/transfer", json={
            "from_account": sender,
            "to_account": receiver,
            "amount": transfer_amount
        })
        print(f"{sender} -> {receiver}: {response.json()}")
        time.sleep(0.1)

if __name__ == "__main__":
    # Parse command-line arguments: cycle length and amount per hop
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=3, help="Number of accounts in cycle")
    parser.add_argument("--amount", type=float, default=100.0, help="Amount transferred per hop")
    args = parser.parse_args()

    # Create a list of account names (e.g., circ_0, circ_1, ...)
    accounts = [f"circ_{i}" for i in range(args.length)]

    # Give each account an initial balance
    for acc in accounts:
        seed_account(acc)

    # Start the circular flow
    run_cycle(accounts, args.amount)