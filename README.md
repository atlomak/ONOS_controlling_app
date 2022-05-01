# ONOS_controlling_app
## About
Simple console application to create routing path between two given hosts. App is connecting with ONOS controller via REST API. App is downloading information about topology from json files and then looking for the shortest and/or the cheapest path by using Dijkstra's algorithm.

## How to use it
1. Run `pip install -r requirements.txt` to install dependencies.
2. Run `main.py` with necessary flags: `--ip` ( ip of ONOS controller) and `--port` (default is 8181). Example: `python main.py -i 192.168.88.25 -p 8181`.
3. If you have changed default ONOS controller username and password use --user and --key flags as in the example above.
4. When run enter ip of first host, ip of second host and the stream in megabytes. Example: `onos_app>>10.0.0.1 10.0.0.2 10`