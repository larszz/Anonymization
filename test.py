import os
import objects as o
import helper as h

CONFIGURATION_PATH = "configurations/configuration.dat"

file_directory = ""
tablename = ""
plainrows = []
anonymrows = []
pseudonymrows = []

def readConfig():
    newConfig = o.Configuration()

    # read file
    with open(CONFIGURATION_PATH, 'r') as lines:

        entries = []

        for l in lines:
            entries.append(l.split(':'))

        

        h.printList(entries)
        for x in range(len(entries)):
            for y in range(len(entries[x])):
                entries[x][y] = str(entries[x][y]).strip()

        print()
        print()
        h.printList(entries)

        pass

    pass


readConfig()