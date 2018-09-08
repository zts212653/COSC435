import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store_true', default=False, dest='select_Mode',
                    help='Indicates the program should wait for an incoming TCP/IP connection on port 9999')

parser.add_argument('-c', action='store', dest='hostname',
                    help='Store hostname')
results = parser.parse_args()

if results.select_Mode:
    print("Server mode")
elif results.hostname != None:
    print(results.hostname)
