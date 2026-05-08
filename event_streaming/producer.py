"""
Kafka producer wrapper – used by the Flask server to publish transaction events.
"""
import json
from kafka import KafkaProducer
from datetime import datetime

# Configure the producer (assumes Kafka broker on localhost:9092)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_transaction(event_type, data, headers, ip):
    """
    Publish a transaction event to the 'transactions' Kafka topic.
    
    Args:
        event_type: 'deposit' or 'transfer'
        data: dict with transaction details (account, amount, from, to, etc.)
        headers: HTTP headers (dictionary)
        ip: client IP address
    """
    record = {
        "type": event_type,
        "timestamp": datetime.now().isoformat(),
        "headers": dict(headers),
        "ip": ip,
        **data
    }
    producer.send('transactions', record)
    producer.flush()   # optional, ensures message is sent immediately