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
        