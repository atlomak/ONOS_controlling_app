import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-u","--username",dest="user")
args = parser.parse_args()

while True:
    dane = input(f"{args.user} Podaj dane: ")
    print(dane)
    if(dane=="x"):
        exit()