import binascii
import logging as log
import os


def printList(list, headline='', seperator=', '):
	print(listToString(list, headline, seperator))


def listToString(list, headline='', seperator=', ', headlineseperator='\n'):
	output = ''
	# add headline
	if (headline != ''):
		output += str(headline) + headlineseperator
	# add lines
	for i in list:
		output += (str(i)) + seperator
	# remove last seperator
	if (seperator != '\n'):
		output = output.rstrip(str(seperator))

	return output


def printList2D(list, headline='', seperator=',\t'):
	for x in list:
		line = ""
		for y in list:
			line += str(y) + seperator

		line = line.rstrip(seperator)
		print(line)


def stripList(list):
	new_list = []
	for l in list:
		new_list.append(str(l).strip())
	return new_list


def dictToString(dict, headline=''):
	try:
		output = ""
		if headline != '':
			output += headline + '\n'
		for key in dict:
			output += '{0}:\t{1}\n'.format(str(key), str(dict[key]))
		output += 3 * '\n'
	except Exception as ex:
		log.warning('An Exception occured!')


def get_random_hex(length=8):
	return str(binascii.b2a_hex(os.urandom(length)))


def get_random_colval():
	return str(get_random_hex(5))
