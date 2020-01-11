import os, binascii
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
	values = None

	def add_to_values(self, key, value):
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

	# tries to split a given value string into multiple values, depending on the set secondary delimiters
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
		"""
		nl = '\n'

		output = ""
		# output += 'Dataset' + nl
		for v in self.values:
			output += '{0}:\t{1}\n'.format(str(v), self.values[v])

		output += 2 * nl
		return output"""
		return self.to_compact_string()

	def __init__(self):
		self.values = {}

	def to_compact_string(self):
		output = ""
		for v in self.values:
			output += f'{str(self.values[v])},\t'
		return output


class TableData:
	filename = None
	columnnames = None
	datasets = None

	def __init__(self, filename):
		self.datasets = []
		self.filename = filename

	def set_columnnames(self, columnnames):
		if not (self.columnnames is None):
			log.error(ex.Messages.ALREADYSETERROR.format('Columnnames'))
			return -1
		self.columnnames = columnnames

	def set_filename(self, filename):
		if not (self.filename is None):
			log.error(ex.Messages.ALREADYSETERROR.format('Filename'))
			return -1

		self.filename = filename

	def add_dataset(self, dataset):
		self.datasets.append(dataset)

	def add_data(self, data):
		if (self.columnnames is None):
			log.error(ex.Messages.NONETYPEERROR.format('Columnnames'))
			return -1

		if (data is None):
			log.error(ex.Messages.NONETYPEERROR.format('Data'))
			return -1

		if not isinstance(data, list):
			log.error(ex.Messages.INSTANCEERROR.format('Data', 'List'))
			return -1

		for idxRow in range(len(data)):
			dataset = DataSet()
			for idxCol in range(len(data[idxRow])):
				try:
					dataset.add_to_values(self.columnnames[idxCol], data[idxRow][idxCol])
				except IndexError as ie:
					log.warning('Error: {0}\nidxRow: {1}\tidxCol: {2}'.format(ie.message, str(idxRow), str(idxCol)))
					continue

			self.add_dataset(dataset)

		return 1

	def __str__(self):
		output = ""
		output += f"Filename: {str(self.filename)}\n"
		output += h.listToString(self.columnnames, 'Column names') + '\n'

		for d in self.datasets:
			output += str(d) + '\n'
		return str(output)


class PseudoTable:
	fieldnames = []
	values = {}

	use_readable_pseudonyms = False
	index = 0

	def __init__(self, use_readable_pseudonyms=False, fieldnames=None):
		if fieldnames is None:
			fieldnames = []
		self.fieldnames = fieldnames
		self.values = {}
		self.use_readable_pseudonyms = use_readable_pseudonyms

	def set_fieldnames(self, fieldnames):
		if len(self.fieldnames) > 0:
			log.warning(ex.Messages.ALREADYSETERROR.format('Fieldnames'))
			return -1

		for fn in fieldnames:
			self.fieldnames.append(str(fn))

		return 1

	def add_value(self, keys):
		# create a tuple to have multiple values as a combined key for the dict
		keytuple = tuple(keys)

		# return keys that are already in dict
		if keytuple in self.values:
			return

		self.values[keytuple] = self.generate_pseudonym()

	def get_pseudo(self, keys):
		keytuple = tuple(keys)
		try:
			return self.values[keytuple]
		except KeyError as ke:
			log.error(str(ke) + ": Key not found in dictionary!")
			return None

	def generate_pseudonym(self):
		output = ''
		if self.use_readable_pseudonyms:
			# return a readable key: combination of all fieldnames with the index as suffix
			for f in self.fieldnames:
				output += str(f) + '_'
			output += str(self.index)
			self.index += 1
		else:
			# output a random hex string with 16 digits
			output += str(binascii.b2a_hex(os.urandom(8)))
		return output
