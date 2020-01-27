import logging as log
from typing import List

import common
import values
from exceptions import Logger, ErrorValues


class PseudonymTable:
	fieldnames = []
	values = {}
	new_fieldname = None

	use_readable_pseudonyms = False
	index = 0


	def __init__(self, use_readable_pseudonyms=False, fieldnames: List = None, new_fieldname=None):
		if fieldnames is None:
			fieldnames = []
		if isinstance(fieldnames, str):
			self.fieldnames = [fieldnames]
		else:
			self.fieldnames = fieldnames
		self.values = {}
		self.use_readable_pseudonyms = use_readable_pseudonyms
		self.new_fieldname = new_fieldname


	def set_fieldnames(self, fieldnames):
		if len(self.fieldnames) > 0:
			Logger.log_already_set('columnnames')
			return -1

		if isinstance(fieldnames, list):
			for fn in fieldnames:
				self.fieldnames.append(str(fn))
		else:
			self.fieldnames.append(fieldnames)
		return 1


	# adds the given values to the pseudonym table, combined as a tuple, referencing their pseudonym
	def add_value(self, keys):
		# create a tuple to have multiple values as a combined key for the dict
		key_tuple = self.generate_key_value(keys)

		# skip keys that are already in dict
		if key_tuple in self.values:
			return

		new_pseudonym = self.generate_pseudonym()
		self.values[key_tuple] = new_pseudonym
		return new_pseudonym


	# adds the data from a dataset to the pseudonym table
	def add_value_from_dataset(self, dataset):
		# check none
		if dataset is None:
			Logger.log_none_type_error('dataset')
			return
		if self.fieldnames is None:
			Logger.log_not_set_yet('columnnames')
			return

		# add values to a list
		value_list = []
		for fn in self.fieldnames:
			field_value = dataset.get_value(fn)
			if field_value is None:
				return ErrorValues.NONETYPE
			value_list.append(field_value)
			# if inserted value is not a list, just insert that value as a string

		# add the combined value
		self.add_value(value_list)


	# generate the pseudonyms from given table data
	def build_pseudonyms_from_data(self, datasets: List):
		# check none
		if datasets is None:
			Logger.log_none_type_error('datasets')
			return -1
		if self.fieldnames is None:
			Logger.log_not_set_yet('columnnames')
			return -1
		# check instance
		if not isinstance(datasets, List):
			Logger.log_instance_error('datasets', 'datasets')
			return -1

		for ds in datasets:
			self.add_value_from_dataset(ds)

		return 1


	##########################################################################################
	# GETTER #################################################################################

	# returns the pseudonym (tuple) for directly given keys
	def get_pseudonym(self, keys):
		key_tuple = self.generate_key_value(keys)
		if key_tuple not in self.values:
			#Logger.log_key_not_found_error(str(key_tuple), 'self.values', '"PseudonymTable.get_pseudonym"')
			new_pseudonym = self.add_value(keys)
			Logger.log_info_new_pseudonym_created(str(key_tuple), new_pseudonym)
			return new_pseudonym
		else:
			return self.values[key_tuple]


	# tries to find all values in dataset to generate a dictionary key with;
	# if all are present, tries to return the pseudonym matching the key
	def get_pseudonym_from_dataset(self, dataset):
		# check none
		if dataset is None:
			Logger.log_none_type_error('dataset')
			return

		# execute
		key_list = []
		for fn in self.fieldnames:
			ds_value = dataset.get_value(fn)
			if ds_value is None:
				Logger.log_key_not_found_error(fn)
				return None

			# if the fieldvalue is a list, add all subvalues to list
			key_list.append(ds_value)
			"""
			if isinstance(value, list):
				for subvalue in value:
					key_list.append(subvalue)
			else:
				key_list.append(value)"""
		return self.get_pseudonym(key_list)


	# returns the new field name of combined fields;
	# if no columnname set, the name will be generated by combining the columnnames
	def get_new_fieldname(self):
		if self.new_fieldname is None:
			self.new_fieldname = common.generate_combined_field_name(self.fieldnames)
		return self.new_fieldname


	# ----------------------------------------------
	# HELPER METHODS
	# generates the matching key value to the given keys
	@staticmethod
	def generate_key_value(keys) -> tuple:
		return common.generate_dict_key(keys)


	# generates the pseudonym;
	# depending on if it should be readable, the pseudonyms are either numbered combinations of the columnnames
	# or a random hex number
	def generate_pseudonym(self):
		output = ''
		if self.use_readable_pseudonyms:
			# return a readable key: combination of all columnnames with the index as suffix
			for f in self.fieldnames:
				output += str(f) + '_'
			output += str(self.index)
			self.index += 1
		else:
			# output a random hex string with 16 digits
			output += common.get_random_colval()
		return output


	##########################################################################################
	# CSV ####################################################################################
	def get_csv_lines(self) -> List:
		retlist = []
		retlist.append(self.get_csv_header())

		for val_key in self.values:
			row = []
			# add pseudonym
			row.append(self.values[val_key])

			# add all field values, joined by the primary delimiter (to make later reading from the tables easier)
			for field_tuple in val_key:
				row.append(values.delimiters.csv.PRIMARY.join(field_tuple))

			retlist.append(row)

		return retlist


	def get_csv_header(self):
		retlist = []
		retlist.append(self.get_new_fieldname())
		for f in self.fieldnames:
			retlist.append(f)
		return retlist
