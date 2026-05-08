from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# In-memory storage: { account_id: balance }
balances = {}

# JSON Lines log file (each line is a JSON object)
LOG_FILE = "transactions.jsonl"

def log_event(event_type, data, headers, ip):
    """Append a JSON line to the log file."""
    record = {
        "type": event_type,
        "timestamp": datetime.now().isoformat(),
        "headers": dict(headers),
        "ip": ip,
        **data
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

def get_balance(account_id):
    return balances.get(account_id, 0.0)

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    account_id = data.get('account_id')
    amount = data.get('amount')
    
    if not account_id or amount is None or amount <= 0:
        return jsonify({'error': 'Invalid deposit data'}), 400
    
    current = get_balance(account_id)
    balances[account_id] = current + amount
    print(f"[DEPOSIT] {account_id} +{amount} → new balance {balances[account_id]}")
    
    # Log the deposit
    log_event("deposit", {"account": account_id, "amount": amount}, request.headers, request.remote_addr)
    
    return jsonify({'status': 'ok', 'new_balance': balances[account_id]})

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    from_acc = data.get('from_account')
    to_acc = data.get('to_account')
    amount = data.get('amount')
    
    if not from_acc or not to_acc or amount is None or amount <= 0:
        return jsonify({'error': 'Invalid transfer data'}), 400
    
    from_balance = get_balance(from_acc)
    if from_balance < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    # Perform transfer
    balances[from_acc] = from_balance - amount
    balances[to_acc] = get_balance(to_acc) + amount
    print(f"[TRANSFER] {from_acc} -> {to_acc} : {amount}")
    
    # Log the transfer
    log_event("transfer", {"from": from_acc, "to": to_acc, "amount": amount}, request.headers, request.remote_addr)
    
    return jsonify({'status': 'ok', 'from_balance': balances[from_acc], 'to_balance': balances[to_acc]})

@app.route('/balance/<account_id>', methods=['GET'])
def balance(account_id):
    bal = get_balance(account_id)
    return jsonify({'account_id': account_id, 'balance': bal})

if __name__ == '__main__':
    # Preload some demo accounts
    balances['alice'] = 1000.0
    balances['bob'] = 500.0
    balances['mallory'] = 200.0
    print("Starting API server on http://localhost:5000")
    app.run(debug=True, port=5000)