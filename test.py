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

		entryList = []

		for l in lines:
			entryList.append(l.split(':'))

		# iterate over every entry
		for e in entryList:
			if (len(e) != 2):
				return -1

			confKey = str(e[0]).strip()
			confValues = getValues(e[1])

			print('Key: ' + str(confKey))
			h.printList(confValues, 'Values:', ',')

		print()
		print()
		h.printList(entryList)

		pass

	pass


# extracts and strips values
def getValues(valueString):
	values = str(valueString).split(',')
	#h.printList(values, 'Before values:')
	values = h.stripList(values)
	#h.printList(values, 'Stripped values:')
	print()
	print()
	return values


readConfig()
