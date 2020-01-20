import logging as log

import exceptions as ex
import helper as h
from objects import TableData



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





	# generate the pseudonyms from given table data
	def build_pseudonyms_from_data(self, tabledata):
		# check none
		if tabledata is None:
			Logger.log_none_type('tabledata')
			return
		if self.fieldnames is None:
			Logger.log_not_set_yet('fieldnames')
			return
	# check instance
		if not isinstance(tabledata, TableData.TableData):
			Logger.log_instance_error('tabledata', 'tabledata')
			return

		for dataset in tabledata.datasets:
			self.add_value_from_dataset(dataset)



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
			output += h.get_random_colval()
		return output
