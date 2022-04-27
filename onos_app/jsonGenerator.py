import json
def generateJson(switchID: str, dst, port: int, timeout: int):
    result = json.dumps({
  "priority": 40000,
  "timeout": timeout,
  "isPermanent": "true",
  "deviceId": switchID,
  "treatment": {
    "instructions": [
      {
        "type": "OUTPUT",
        "port": port
      }
    ]
  },
  "selector": {
    "criteria": [
      {
        "type": "ETH_TYPE",
        "ethType": "0x0800"
      },
      {
        "type": "IPV4_DST",
        "ip": dst
      }
    ]
  }
})
    return result

    
if __name__ == "__main__":
    print(generateJson(switchID="test", dst="test", port="test", timeout=10))