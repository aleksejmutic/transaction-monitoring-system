"""
Neo4j DAO (Data Access Object) for transaction monitoring.
Handles all graph database operations.
"""
from neo4j import GraphDatabase

def store_transfer(transaction, from_acc, to_acc, amount, timestamp, headers, ip):
    """Create transfer relationship between two accounts."""
    transaction.run("MERGE (a:Account {id: $frm})", frm=from_acc)
    transaction.run("MERGE (b:Account {id: $to})", to=to_acc)
    transaction.run("""
        MATCH (a:Account {id: $frm}), (b:Account {id: $to})
        CREATE (a)-[:SENT_TO {amount: $amt, timestamp: $ts, ip: $ip}]->(b)
    """, frm=from_acc, to=to_acc, amt=amount, ts=timestamp, ip=ip)

    # Link device if present
    device = headers.get('X-Device-Id')
    if device:
        transaction.run("MERGE (d:Device {id: $dev})", dev=device)
        transaction.run("""
            MATCH (a:Account {id: $acc}), (d:Device {id: $dev})
            CREATE (a)-[:USED_AT {timestamp: $ts}]->(d)
        """, acc=from_acc, dev=device, ts=timestamp)

def store_deposit(transaction, account, amount, timestamp, headers, ip):
    """Create deposit self‑relationship for an account."""
    transaction.run("MERGE (a:Account {id: $acc})", acc=account)
    transaction.run("""
        MATCH (a:Account {id: $acc})
        CREATE (a)-[:DEPOSIT {amount: $amt, timestamp: $ts, ip: $ip}]->(a)
    """, acc=account, amt=amount, ts=timestamp, ip=ip)

    # Link device if present
    device = headers.get('X-Device-Id')
    if device:
        transaction.run("MERGE (d:Device {id: $dev})", dev=device)
        transaction.run("""
            MATCH (a:Account {id: $acc}), (d:Device {id: $dev})
            CREATE (a)-[:USED_AT {timestamp: $ts}]->(d)
        """, acc=account, dev=device, ts=timestamp)