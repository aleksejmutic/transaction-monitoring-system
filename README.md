# Normal background traffic
python3 normal_client.py

# Attack patterns
python3 circular_money_flow_client.py --length 4 --amount 150
python3 shared_device_client.py --accounts 6 --device "ring_device"
python3 card_testing.py --count 30 --amount 1.99 --merchant "victim_shop"