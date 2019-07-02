import sys
import getopt
from Server import startApp

address = 'localhost'
login = 'root'
password = '!C75dcdc'
database = 'restfullists'

opts, args = getopt.getopt(sys.argv[1:], "ha:l:p:d:")
for opt, arg in opts:
    if opt == '-h':
        print('python server.py [-a <server_address>] [-l <login>] [-p <password>] [-d <database>]')
        sys.exit()
    if opt == '-a':
        address = arg
    elif opt == "-l":
        login = arg
    elif opt == "-p":
        password = arg
    elif opt == "-d":
        database = arg

startApp(address, login, password, database)