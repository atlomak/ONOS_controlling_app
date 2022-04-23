from tkinter.messagebox import NO
import requests
from ipaddress import ip_address
import json

class OnosIpException(Exception):
    pass

class Switch:
    def __init__(self, id, available):
        self.id = id
        self.available = available
        self.links = []
    def __str__(self):
        print(f"id: {self.id} available: {self.available}")

class Host:
    pass

class Link:
    def __init__(self):
        pass


class Controller:
    def __init__(self,ip: str,port: str,user: str,password: str) -> None:
        try:
            self.ip = f"http://{ip}:{port}/onos/v1"
            self.auth = (user,password)
            self.switches = []
            self.hosts = []
            r = requests.get(url=f"{self.ip}/devices",auth=self.auth)
            r.raise_for_status()
        except Exception as err:
            raise SystemExit(err)
    def loadDevices(self) -> None:
        url = f"{self.ip}/devices"
        r = requests.get(url=url,auth=self.auth)
        devices_json = r.json()
        devices = devices_json["devices"]
        for device in devices:
            self.switches.append(Switch(id=device["id"],available=device["available"]))
    def switches(self) -> None:
        print(self.switches)
        


if __name__ == "__main__":
    test = Controller(ip="192.168.88.27",port="8181",user="onos",password="rocks")
    test.loadDevices()
    for switch in test.switches:
        print(switch.available)