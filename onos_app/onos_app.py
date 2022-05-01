import requests
import json
from jsonGenerator import generateJson

#Exceptions
class OnosControllerError(Exception):
    """Failed to create Controller object"""
class OnosWrongAuth(Exception):
    """The credentials provided are invalid"""
class OnosHostsError(Exception):
    """Failed to load Hosts"""
class OnosSwitchError(Exception):
    """Failed to load Switches"""
class OnosWrongIP(Exception):
    """The Host's ip provied is invalid"""

class Switch:
    def __init__(self, id, available):
        self.id = id
        self.available = available
        self.links = set()
        self.hosts = set()
    def __str__(self):
        result = f"Switch id: {self.id} available: {self.available}, \nlinks: {len(self.links)}\n"
        for link in self.links:
            result = result + str(link)
        result += f"host(s): {len(self.hosts)}\n"
        for host in self.hosts:
            result += str(host) +" \n"
        return result
        
class Host:
    def __init__(self, ip, mac, switch, locationId, locationPort):
        self.ip = ip
        self.mac = mac
        self.switch = switch
        self.locationId = locationId
        self.locationPort = locationPort
    def __str__(self):
        result = f" ip: {self.ip} \n" \
        + f" mac: {self.mac} \n" \
        + f" switch: {self.locationId} \n" \
        + f" port: {self.locationPort}"
        return result

class Link:
    def __init__(self,src,srcPort,dst,dstPort,state,linkType,value = 1):
        self.src = src
        self.srcPort = srcPort
        self.dst = dst
        self.dstPort = dstPort
        self.state = state
        self.linkType = linkType
        self.value = value
    def __str__(self):
        result = f" src: {self.src} \n"\
            + f" port: {self.srcPort} \n"\
            + f" dst: {self.dst} \n"\
            + f" port: {self.dstPort} \n"
        return result
        
class Controller:

    def __init__(self,ip: str,port: str,user: str,password: str) -> None:
        try:
            self.s = requests.session()
            self.ip = f"http://{ip}:{port}/onos/v1"
            self.s.auth = (user,password)
            self.switches = set()
            self.hosts = set()
            r = self.s.head(url=f"{self.ip}/devices")
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == "401":
                raise OnosWrongAuth(f"Wrong login or password. Given credentials: {self.auth}")
            else:
                print(err)
        except requests.exceptions.ConnectionError:
            print("Connection error occurred.")
        finally:
            self.s.close()
            exit()

    def loadDevices(self) -> None:
        try:
            url = f"{self.ip}/devices"
            r = self.s.get(url=url)
            r.raise_for_status()
            devices_json = r.json()
            devices = devices_json["devices"]

            if len(devices) == 0:
                raise OnosSwitchError("Switches not found")
                
            for device in devices:
                if(device["type"]=="SWITCH"):
                    self.switches.add(Switch(id=device["id"],available=device["available"]))
        except requests.exceptions.HTTPError as err:
            print(err)
        except requests.exceptions.ConnectionError:
            print("Connection error occurred.")
        finally:
            self.s.close()

    def loadLinks(self) -> None:
        try:
            url = f"{self.ip}/links"
            r = self.s.get(url=url)
            r.raise_for_status()
            links_json = r.json()
            links = links_json["links"]
            for link in links:
                src_dict = link["src"]
                dst_dict = link["dst"]
                state = link["state"]
                linkType = link["type"]
                for switch in self.switches:
                    if switch.id == src_dict["device"]:
                        switch.links.add(Link(src=src_dict["device"], \
                                                srcPort=src_dict["port"], \
                                                dst=dst_dict["device"], \
                                                dstPort=dst_dict["port"], \
                                                state=state, \
                                                linkType=linkType))            
        except requests.exceptions.HTTPError as err:
            print(err)
        except requests.exceptions.ConnectionError:
            print("Connection error occurred.")
        finally:
            self.s.close()

    def loadHosts(self) -> None:
        try:
            url = f"{self.ip}/hosts"
            r = self.s.get(url)
            r.raise_for_status()
            hosts_json = r.json()
            hosts = hosts_json["hosts"]

            # Checking if there are hosts connected to ONOS #
            if len(hosts) == 0:
                raise OnosHostsError("Hosts not found")

            for host_dict in hosts:
                ip = host_dict["ipAddresses"][0]
                mac = host_dict["mac"]
                locations_dict = host_dict["locations"][0]
                elementId = locations_dict["elementId"]
                port = locations_dict["port"]
                # Adding refrence to switch for host object #
                for switch in self.switches:
                    if switch.id == elementId:
                        hostSwitch = switch
                host = Host(ip=ip, mac=mac,switch=hostSwitch, locationId=elementId, locationPort=port)
                # Adding refrence to host for switch object #
                self.hosts.add(host)
                for switch in self.switches:
                    if switch.id == host.locationId:
                        switch.hosts.add(host)            

        except requests.exceptions.HTTPError as err:
            print(err)
        except requests.exceptions.ConnectionError:
            print("Connection error occurred.")
        finally:
            self.s.close()

    def showDevices(self) -> None:
        if len(self.switches) == 0:
            print("No switches loaded")
        else:
            for switch in self.switches:
                print(switch)

    def postFlow(self, h1, h2, route, stream):
        try:
            switches = {}
            for switch in self.switches:
                switches[switch.id] = switch
            for sID in route:
                currentSwitch = switches[sID]
                if currentSwitch.id == route[0]:
                    for host in currentSwitch.hosts:
                        if host.ip == h1:
                            flowRule = generateJson(sID, host.ip, host.locationPort, 60)
                            r = self.s.post(f"{self.ip}/flows/{sID}",headers={'Content-type': 'application/json',"Accept": "application/json"}, json=flowRule)
                            r.raise_for_status()
                            break
                    for link in currentSwitch.links:
                        index = route.index(sID)
                        if link.dst == route[index+1]:
                            flowRule = generateJson(sID, h2, port=link.srcPort, timeout=60)
                            r = self.s.post(f"{self.ip}/flows/{sID}",headers={'Content-type': 'application/json',"Accept": "application/json"}, json=flowRule)
                            r.raise_for_status()
                            link.value =+ int(stream)
                elif currentSwitch.id == route[-1]:
                    for host in currentSwitch.hosts:
                        if host.ip == h2:
                            flowRule = generateJson(sID, host.ip, host.locationPort, 60)
                            r = self.s.post(f"{self.ip}/flows/{sID}",headers={'Content-type': 'application/json',"Accept": "application/json"}, json=flowRule)
                            r.raise_for_status()
                            break
                    for link in currentSwitch.links:
                        index = route.index(sID)
                        if link.dst == route[index-1]:
                            flowRule = generateJson(sID, h1, port=link.srcPort, timeout=60)
                            r = self.s.post(f"{self.ip}/flows/{sID}",headers={'Content-type': 'application/json',"Accept": "application/json"}, json=flowRule)
                            r.raise_for_status()
                            link.value =+ int(stream)
                else:
                    for link in currentSwitch.links:
                        index = route.index(sID)
                        if link.dst == route[index-1]:
                            flowRule = generateJson(sID, h1, port=link.srcPort, timeout=60)
                            r = self.s.post(f"{self.ip}/flows/{sID}",headers={'Content-type': 'application/json',"Accept": "application/json"}, json=flowRule)
                            r.raise_for_status()
                        elif link.dst == route[index+1]:
                            flowRule = generateJson(sID, h2, port=link.srcPort, timeout=60)
                            r = self.s.post(f"{self.ip}/flows/{sID}",headers={'Content-type': 'application/json',"Accept": "application/json"}, json=flowRule)
                            r.raise_for_status()
                            link.value =+ int(stream)            
            return True
        except requests.exceptions.HTTPError as err:
            print(err)
            return False
        except requests.exceptions.ConnectionError:
            print("Connection error occurred.")
            return False
        finally:
            self.s.close()


            
    # Algorithm #
    def DijkstraAlgorithm(self, h1: str, h2: str, stream = 10) -> list():
        q = self.switches.copy()
        s = set()
        # Dict to help assigning nextSwitch based on link objects #
        switches = {}
        for switch in q:
            switches[switch.id] = switch
        u = {}
        # checking src switch and dst switch #
        switch1, switch2 = None
        for host in self.hosts:
            if h1 == host.ip:
                switch1 = host.switch
            if h2 == host.ip:
                switch2 = host.switch
        if switch1 == None or switch2 == None:
            x = lambda s1,s2: (h1 if s1 == None else "", h2 if s2 == None else "")
            raise OnosWrongIP(f"Host(s) with this IP was not found",{x(switch1,switch2)})
        for switch in self.switches:
            u[switch.id] = [999,0]
        u[switch1.id] = [0,0]  # distance, previous switch #
        u_copy = u.copy()
        while len(q)>0:
            min_u = sorted(u_copy.items(), key=lambda x: x[1])   # (id,distance,previous)
            id = min_u[0][0]
            currentSwitch = switches[id]
            q.remove(currentSwitch)
            s.add(currentSwitch)
            for link in currentSwitch.links:
                if link.state == "ACTIVE":
                    nextSwitch = switches[link.dst]
                    if nextSwitch in q:
                        d = u[nextSwitch.id][0]
                        if d > (u[currentSwitch.id][0] + link.value):
                            u[nextSwitch.id][0] = (u[currentSwitch.id][0] + link.value)
                            u[nextSwitch.id][1] = currentSwitch.id
            del u_copy[id]
        # creating route list #
        result = []
        def route(id):
            result.append(id)
            next_id = u[id][1]
            if next_id != 0:
                route(next_id)
        route(switch2.id)
        result.reverse()
        if self.postFlow(h1, h2, result, stream) == True:
            print("SUCCESFUL ADDING ROUTING PATH")
#Test#
if __name__ == "__main__":
    
    test = Controller(ip="192.168.88.25",port="8180",user="onos",password="rock1s")
    test.loadDevices()
    test.loadLinks()
    test.loadHosts()
            #print(test.DijkstraAlgorithm("10.0.0.2", "10.0.0.9"))
    
    