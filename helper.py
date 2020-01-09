


def printList(list, headline = '', seperator = ', '):
	print(listToString(list, seperator))

def listToString(list, headline = '', seperator = ', ', headlineseperator = '\n'):
	output = ''
	# add headline
	if(headline != ''):
		output += str(headline) + headlineseperator
	# add lines
	for i in list:
		output += (str(i)) + seperator
	# remove last seperator
	if(seperator != '\n'):
		output = output.rstrip(str(seperator))

	return output


def printList2D(list, headline = '', seperator = ',\t'):
	for x in list:
		line = ""
		for y in list:
			line += str(y) + seperator

		line = line.rstrip(seperator)
		print(line)

def stripList(list):
	newList = []
	for l in list:
		newList.append(str(l).strip())

	return newList