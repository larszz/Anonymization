import helper as h
import values as v
import exceptions as ex
import logging as log

INITIAL_VALUE = -1


class Configuration:
	file_directories = INITIAL_VALUE
	output_directory = INITIAL_VALUE
	tablenames = INITIAL_VALUE
	plainrows = INITIAL_VALUE
	anonymrows = INITIAL_VALUE
	pseudonymrows = INITIAL_VALUE

	# sets a configuration
	# ignores, if a configuration value is already set
	# returns 1 if setting worked
	#
	# EXCEPTIONS:
	#   NoneTypeError: value is NoneType
	#   TypeError: value is not a list
	def setConfigurationValue(self, key, value):

		# check if value is in valid format
		if (value is None):
			raise ex.NoneTypeError(str(key))

		if (not isinstance(value, list)):
			raise TypeError

		# set configuration

		# filedirectory
		if key == v.conf.DIRECTORY:
			self.file_directories = value

		# output directory
		if key == v.conf.OUTPUTDIRECTORY:
			self.output_directory = value[0]

		# tablename
		elif key == v.conf.TABLE:
			self.tablenames = value

		# plainrows
		elif key == v.conf.PLAIN:
			self.plainrows = value

		# anonym
		elif key == v.conf.ANONYM:
			self.anonymrows = value

		# pseudonym
		elif key == v.conf.PSEUDONYM:
			self.pseudonymrows = value

		return 1

	def __init__(self):
		pass

	def __str__(self):
		newline = '\n'

		output = newline

		output += "CONFIGURATION" + newline

		output += h.listToString(self.file_directories, v.conf.DIRECTORY, headlineseperator=':\t') + newline
		output += v.conf.OUTPUTDIRECTORY + ":\t" + self.output_directory + newline
		output += h.listToString(self.tablenames, v.conf.TABLE, headlineseperator=':\t') + newline
		output += h.listToString(self.plainrows, v.conf.PLAIN, headlineseperator=':\t') + newline
		output += h.listToString(self.anonymrows, v.conf.ANONYM, headlineseperator=':\t') + newline
		output += h.listToString(self.pseudonymrows, v.conf.PSEUDONYM, headlineseperator=':\t') + newline

		output += 3 * newline

		return output


class DataSet:
	values = {}

	def addToDict(self, key, value):
		if key in self.values:
			log.warning(ex.Messages.KEYERROR.format(key))
			return

		self.values[str(key)] = self.extractEntries(value)
		log.debug(ex.Messages.Debug.VALUE_ADDED_TO_KEY.format(key, value))
		pass

	def anonymize(self, columnnames):
		pass

	def pseudonymize(self, columnnames):
		pass

	@staticmethod
	def extractEntries(valuestring):
		for delim in v.delimiters.csv.SECONDARIES:
			values = str(valuestring).split(delim)

			# return split values, if there is more than 1 entry after split
			if len(values) > 1:
				return values

		# if entry could not be split, return the given valuestring as list
		return [valuestring]

	def __str__(self):
		nl = '\n'

		output = ""
		output += 'Dataset' + nl
		for v in self.values:
			output += '{0}:\t{1}\n'.format(str(v), self.values[v])

		output += 2 * nl
		return output

	def __init__(self):
		pass
