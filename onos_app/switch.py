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