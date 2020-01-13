import exceptions as ex
import helper as h
import values as v



INITIAL_VALUE = None


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
