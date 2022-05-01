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
