import argparse
from onos_app import controller
from onos_app import exceptions

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i","--ip",type=str, help="IP to onos controller", required=True)
    parser.add_argument("-p","--port",type=str, help="Port to onos controller", required=True)
    parser.add_argument("-u","--user",type=str,help="Username to onos controller", default="onos")
    parser.add_argument("-k","--key",type=str, help="password to onos controller", default="rocks")
    args = parser.parse_args()

    try:
        controller = controller.Controller(args.ip, args.port, args.user, args.key)
        controller.loadDevices()
        controller.loadHosts()
        controller.loadLinks()
    except exceptions.OnosWrongAuth as err:
        print(err)
    except exceptions.OnosHostsError as err:
        print(err)
    except exceptions.OnosSwitchError as err:
        print(err)
    except exceptions.OnosControllerError as err:
        print(err)
    else:
        while True:
            try:
                print("Enter addresses and stream:")
                x = input("onos_app>>")
                x = x.split(" ")
                if len(x) > 3:
                    print("Too many arguments,\n use the help command to access help information")
                elif len(x) == 0:
                    print("You have to specify host's ip and stream,\n use the help command to access help information")
                elif len(x) == 1:
                    if x[0] == "help":
                        print("Commands:\n"+
                        "print -Prints all loaded devices [switches,hosts] \n"+
                        "exit -exits the app \n"+
                        "To use the app you have to specify two hosts and stream between them.\n"+
                        "Command should be:<ip of host 1> <ip of host 2> <stream [in megabytes]>\n"+
                        "EXAMPLE:\n"+
                        "onos_app>>10.0.0.1 10.0.0.2 10")
                    elif x[0] == "exit":
                        print("***CLOSING APP***")
                        exit()
                    elif x[0] == "print":
                        controller.showDevices()
                    else:
                        print("Unknown command, use the help command to access help information")
                elif len(x) == 3:
                    controller.DijkstraAlgorithm(x[0], x[1], stream=x[2])
                else:
                    print("Missing one argument")
            except exceptions.OnosWrongIP as err:
                print(err)
                print("To check all connected devices, type print")       