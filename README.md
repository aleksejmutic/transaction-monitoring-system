# Generate Traffic for Fraud Detection Testing

## Normal Background Traffic

```bash
python3 normal_client.py
```

## Attack Patterns

### Circular Money Flow Attack

```bash
python3 circular_money_flow_client.py --length 4 --amount 150
```

### Shared Device Fraud Simulation

```bash
python3 shared_device_client.py --accounts 6 --device "ring_device"
```

### Card Testing Attack

```bash
python3 card_testing.py --count 30 --amount 1.99 --merchant "victim_shop"
```