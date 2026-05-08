import requests
import random
import time

BASE_URL = "http://localhost:5000"
ACCOUNTS = ['alice', 'bob', 'mallory', 'charlie', 'dave']

def deposit(account, amount):
    resp = requests.post(f"{BASE_URL}/deposit", json={'account_id': account, 'amount': amount})
    print(f"Deposit {amount} to {account}: {resp.json()}")

def transfer(from_acc, to_acc, amount):
    resp = requests.post(f"{BASE_URL}/transfer", json={
        'from_account': from_acc,
        'to_account': to_acc,
        'amount': amount
    })
    print(f"Transfer {amount} from {from_acc} to {to_acc}: {resp.json()}")

def check_balance(account):
    resp = requests.get(f"{BASE_URL}/balance/{account}")
    print(f"Balance for {account}: {resp.json()}")

def simulate_person():
    # A simple sequence: deposit some money, then transfer, then check
    person = random.choice(ACCOUNTS)
    print(f"\n--- Simulating {person} ---")
    
    # Deposit a random amount
    dep_amt = round(random.uniform(50, 500), 2)
    deposit(person, dep_amt)
    time.sleep(0.5)
    
    # Transfer to someone else
    recipient = random.choice([a for a in ACCOUNTS if a != person])
    trans_amt = round(random.uniform(10, 200), 2)
    transfer(person, recipient, trans_amt)
    time.sleep(0.5)
    
    # Check final balance
    check_balance(person)

if __name__ == "__main__":
    # Run a few simulations
    for _ in range(5):
        simulate_person()
        time.sleep(1)