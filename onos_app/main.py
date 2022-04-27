import argparse
import onos_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i","--ip",type=str, help="IP to onos controller")
    parser.add_argument("-p","--port",type=str, help="Port to onos controller", default="8181")
    parser.add_argument("-u","--user",type=str,help="Username to onos controller", default="onos")
    parser.add_argument("-k","--key",type=str, help="password to onos controller", default="rocks")
    args = parser.parse_args()

    controller = onos_app.Controller(args.ip, args.port, args.user, args.key)
    controller.loadDevices()
    controller.loadHosts()
    controller.loadLinks()

    while True:
        x = input("Enter data:<ip 1> <ip 2> <stream[in megabytes]>" + 
        "\n Type exit to leave")
        x = x.split(" ")
        if x == "exit":
            exit()
        elif len(x) == 3:
            controller.DijkstraAlgorithm(x[0], x[1], x[2])
        else:
            print("Wrong argument(s)")