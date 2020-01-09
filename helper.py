


def printList(list, headline = '', seperator = '\n'):
	output = ''
	if(headline != ''):
		output += str(headline) + '\n'

	for i in list:
		output += (str(i)) + seperator

	if(seperator != '\n'):
		output = output.rstrip(str(seperator))

	print(output)


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