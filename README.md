# ONOS_controlling_app
## About
Simple console application to create routing path between two given hosts. App is connecting with ONOS controller via REST API. App is downloading information about topology from json files and then looking for the shortest and/or the cheapest path by using Dijkstra's algorithm.

## How to use it
1. Run `pip install -r requirements.txt` to install dependencies.
2. Run `main.py` with necessary flags [--ip and --port]. Example: `python main.py -i 192.168.88.25 -p 8181`.
3. If you have changed default ONOS controller username and password use --user and --key flags as in the example above.