# Transaction Monitoring System

This project simulates a real-time financial transaction API, streams every deposit/transfer through Kafka, and loads the data into a Neo4j graph database. Fraud patterns (circular flows, shared device rings, card testing) are later detected by querying the graph.

## Architecture

- **Flask API** (`server.py`) – receives deposits/transfers, publishes each event to a Kafka topic.
- **Kafka** – decouples the API from the database; provides a replayable event log.
- **Kafka Consumer** (`consumer.py`) – reads the Kafka topic and writes nodes/relationships into Neo4j.
- **Neo4j** – stores accounts, devices, transfers, deposits, and device-usage links.

---

## Prerequisites

- Docker & Docker Compose
- Python 3.10+ with `venv`
- `pip` (Python package manager)

---

## How to run the program

Important: python, kafka-python and flask are locally installed on my pc, so they should exist locally, since they are not included inside of the docker-compose file. The clientside code also runs on localhost. 

### 1. Create and activate virtual environment (from project root)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Python dependencies

```bash
pip install flask requests kafka-python neo4j
```

### 3. Start Kafka, Zookeeper and Neo4j (Docker Compose)

```bash
docker-compose up -d
```

### 4. Run the Kafka consumer

> Keep this terminal open.

```bash
python3 -m event_streaming.consumer
```

### 5. Run the Flask server

> Open a **new terminal** and activate the same virtual environment.

```bash
cd api_simulator
python3 server.py
```

### 6. Generate traffic (example: card testing attack)

> Open a **new terminal** and activate the virtual environment.

```bash
cd api_simulator
python3 card_testing.py --count 30 --amount 1.99 --merchant "victim_shop"
```

---

# Normal Background Traffic

```bash
python3 normal_client.py
```


# Attack Patterns

## Circular Money Flow Attack

```bash
python3 circular_money_flow_client.py --length 4 --amount 150
```

## Shared Device Fraud Simulation

```bash
python3 shared_device_client.py --accounts 6 --device "ring_device"
```

## Card Testing Attack

```bash
python3 card_testing.py --count 30 --amount 1.99 --merchant "victim_shop"
```
