"""
Kafka consumer that loads transactions into Neo4j in real time.
Uses DAO for database operations.
"""
import json
from kafka import KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from neo4j import GraphDatabase
from .dao import store_transfer, store_deposit   # relative import

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'transactions'
NEO4J_URI = 'bolt://localhost:7687'
NEO4J_AUTH = ('neo4j', 'password123')

def ensure_topic():
    """Create the Kafka topic if it doesn't exist."""
    admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
    try:
        topic = NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
        print(f"Topic '{TOPIC}' created.")
    except TopicAlreadyExistsError:
        print(f"Topic '{TOPIC}' already exists.")
    except Exception as e:
        print(f"Error creating topic: {e}")
    finally:
        admin.close()

def main():
    ensure_topic()

    # Kafka consumer
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    # Neo4j driver
    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

    print(f"Listening for messages on topic '{TOPIC}'...")
    with driver.session() as session:
        for msg in consumer:
            rec = msg.value
            if rec['type'] == 'transfer':
                session.execute_write(
                    store_transfer,
                    rec['from'], rec['to'], rec['amount'],
                    rec['timestamp'], rec['headers'], rec['ip']
                )
                print(f"Stored transfer: {rec['from']} -> {rec['to']} ({rec['amount']})")
            elif rec['type'] == 'deposit':
                session.execute_write(
                    store_deposit,
                    rec['account'], rec['amount'],
                    rec['timestamp'], rec['headers'], rec['ip']
                )
                print(f"Stored deposit: {rec['account']} +{rec['amount']}")

    driver.close()

if __name__ == '__main__':
    main()