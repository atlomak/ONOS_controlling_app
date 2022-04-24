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
        result = f"Switch id: {self.id} available: {self.available}, \n \
        links: \n"
        for link in self.links:
            result = result + str(link)
        return result
        


class Host:
    pass

class Link:
    def __init__(self,src,srcPort,dst,dstPort,state,linkType):
        self.src = src
        self.srcPort = srcPort
        self.dst = dst
        self.dstPort = dstPort
        self.state = state
        self.linkType = linkType
    def __str__(self):
        result = f"src: {self.src} \n \
            port: {self.srcPort} \n \
            dst: {self.dst} \n\
            port: {self.dstPort} \n"
        return result
        

class Controller:
    def __init__(self,ip: str,port: str,user: str,password: str) -> None:
        try:
            self.s = requests.session()
            self.ip = f"http://{ip}:{port}/onos/v1"
            self.s.auth = (user,password)
            self.hosts = []
            self.switches = []
            r = self.s.get(url=f"{self.ip}/devices")
            r.raise_for_status()
        except Exception as err:
            raise SystemExit(err)
    def loadDevices(self) -> None:
        try:
            url = f"{self.ip}/devices"
            r = self.s.get(url=url)
            r.raise_for_status()
            devices_json = r.json()
            devices = devices_json["devices"]
            for device in devices:
                if(device["type"]=="SWITCH"):
                    self.switches.append(Switch(id=device["id"],available=device["available"]))
        except requests.HTTPError() as err:
            print(f"Problem with connection, {err}")
    def loadLinks(self):
        url = f"{self.ip}/links"
        r = self.s.get(url=url)
        links_json = r.json()
        links = links_json["links"]
        for link in links:
            src_dict = link["src"]
            dst_dict = link["dst"]
            state = link["state"]
            linkType = link["type"]
            for switch in self.switches:
                if switch.id == src_dict["device"]:
                    switch.links.append(Link(src=src_dict["device"], \
                                            srcPort=src_dict["port"], \
                                            dst=dst_dict["device"], \
                                            dstPort=dst_dict["port"], \
                                            state=state, \
                                            linkType=linkType))


    def showDevices(self) -> None:
        for switch in self.switches:
            print(switch)
            
        


if __name__ == "__main__":
    test = Controller(ip="192.168.88.27",port="8181",user="onos",password="rocks")
    test.loadDevices()
    test.loadLinks()
    test.showDevices()