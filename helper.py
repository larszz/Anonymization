import binascii
import logging as log
import os
import pprint


def print_list(list, headline='', seperator=', '):
	print(list_to_string(list, headline, seperator))


def list_to_string(list, headline='', seperator=', ', headlineseperator='\n'):
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


def print_list_2d(list, headline='', seperator=',\t'):
	output = ''
	if headline != '':
		output += headline + '\n'
	for x in list:
		line = ""
		for y in x:
			line += str(y) + seperator

		line = line.rstrip(seperator)
		output += line + '\n'

	print(output)
	pprint.pprint(list)


def strip_list(list):
	new_list = []
	for l in list:
		new_list.append(str(l).strip())
	return new_list


def dict_to_string(dict, headline=''):
	try:
		output = ""
		if headline != '':
			output += headline + '\n'
		for key in dict:
			output += '{0}:\t{1}\n'.format(str(key), str(dict[key]))
		output += 3 * '\n'
	except Exception as ex:
		log.warning('An Exception occured!')
