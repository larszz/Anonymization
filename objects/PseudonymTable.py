import logging as log
from typing import Any, Tuple

from exceptions import Logger

import exceptions as ex
import helper as h
from objects import TableData



class PseudonymTable:
	fieldnames = []
	values = {}
	new_fieldname = None

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





	# adds the given values to the pseudonym table, combined as a tuple, referencing their pseudonym
	def add_value(self, keys):

		# create a tuple to have multiple values as a combined key for the dict
		key_tuple = self.generate_key_value(keys)

		# skip keys that are already in dict
		if key_tuple in self.values:
			return

		self.values[key_tuple] = self.generate_pseudonym()



	# adds the
	def add_value_from_dataset(self, dataset):
		# check none
		if dataset is None:
			Logger.log_none_type('dataset')
			return
		if self.fieldnames is None:
			Logger.log_not_set_yet('fieldnames')
			return

		# add values to a list
		value_list = []
		for fn in self.fieldnames:
			field_value = dataset.get_value(fn)
			# if the inserted value is a list, iterate over every list element and insert it as a string
			if isinstance(field_value, list):
				for val in field_value:
					value_list.append(str(val))
			# if inserted value is not a list, just insert that value as a string
			else:
				value_list.append(str(field_value))
		# make tuple from value list for key
		self.add_value(value_list)





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





	# ----------------------------------------------
	# GETTER

	# returns the pseudonym for directly given keys
	def get_pseudonym(self, keys):
		key_tuple = self.generate_key_value(keys)
		try:
			return self.values[key_tuple]
		except KeyError as ke:
			log.error(str(ke) + ": Key not found in dictionary!")
			return None



	# tries to find all values in dataset to generate a dictionary key with;
	# if all are present, tries to return the pseudonym matching the key
	def get_pseudonym_from_dataset(self, dataset):
		# check none
		if dataset is None:
			Logger.log_none_type('dataset')
			return

		key_list = []
		for fn in self.fieldnames:
			val = dataset.get_value(fn)
			if val is None:
				Logger.log_key_not_found_error(fn)
				return None
			key_list.append(val)

		key = self.generate_key_value(key_list)
		return self.get_pseudonym(key)



	# ----------------------------------------------
	# HELPER METHODS
	# generates the matching key value to the given keys
	@staticmethod
	def generate_key_value(keys) -> tuple:
		# check none
		if keys is None:
			Logger.log_none_type('keys')
			return

		# if keys are already a tuple, return that tuple
		if not isinstance(keys, tuple):
			# keys are a list
			if isinstance(keys, list):
				return tuple(str(i) for i in keys)
			# keys is actually only one key
			else:
				t: Tuple[Any] = (str(keys),)
				return t
		return keys



	# generates the pseudonym;
	# depending on if it should be readable, the pseudonyms are either numbered combinations of the fieldnames
	# or a random hex number
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
