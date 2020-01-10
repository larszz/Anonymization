import os
import objects as o
import helper as h
import FileReader as fr

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
			entryList.append(l.split(':', 1))

		# iterate over every entry
		for e in entryList:
			if (len(e) != 2):
				return -1

			confKey = str(e[0]).strip()
			confValues = getConfigValues(e[1])

			newConfig.setConfigurationValue(confKey, confValues)

	print(newConfig)

	return newConfig


# extracts and strips values
def getConfigValues(valueString):
	values = str(valueString).split(',')
	values = h.stripList(values)
	return values


conf = readConfig()
fr.readFile(conf)
