import logging as log
from typing import List, Dict

import common
import helper as h
from objects import DataSet, PseudonymTable
import random
from exceptions import Logger


class TableData:
	filename = None
	column_names = None
	datasets: dict

	pseudonym_tables: Dict = {}


	def __init__(self, filename):
		self.datasets = {}
		self.filename = filename


	def set_columnnames(self, columnnames):
		if not (self.column_names is None):
			return Logger.log_already_set('Columnnames')
		self.column_names = columnnames


	def set_filename(self, filename):
		if not (self.filename is None):
			return Logger.log_already_set('Filename')

		self.filename = filename


	def add_dataset(self, dataset):
		self.datasets.append(dataset)


	# add the given data, separated into a two-dimensional list
	def add_data(self, data):
		if self.column_names is None:
			return Logger.log_none_type_error('Columnnames')

		if data is None:
			return Logger.log_none_type_error('Data')

		if not isinstance(data, list):
			return Logger.log_instance_error('Data', 'list')

		for idxRow in range(len(data)):
			dataset = DataSet.DataSet()
			for idxCol in range(len(data[idxRow])):
				try:
					dataset.add_to_values(self.column_names[idxCol], data[idxRow][idxCol])
				except IndexError as ie:
					log.warning('Error: {0}\nidxRow: {1}\tidxCol: {2}'.format(ie.message, str(idxRow), str(idxCol)))
					continue

			self.add_dataset(dataset)

		return 1


	# anonymizes one given field;
	# if pattern is set: tries to change the field value depending on the pattern
	# if no pattern is given, the value will be changed to a random hex number
	def anonymize_one(self, field, pattern=None):
		if pattern is None:
			for ds in self.datasets:
				ds.set_fieldvalue_random(field)
		else:
			for ds in self.datasets:
				ds.set_fieldvalue_by_pattern(field, pattern)


	# combines multiple given fields into one field, representing the previous values by a pseudonym
	# i.e. pseudonymize a city and its plz by one pseudonym
	def pseudonymize_many(self, fieldnames: List[str], pseudonym_table=None, readable: bool = False,
						  new_field_name: str = None):
		# check none
		if fieldnames is None:
			return Logger.log_none_type_error('fields')
		if pseudonym_table is None:
			return Logger.log_none_type_error('pseudonym_table')
		if new_field_name is None:
			new_field_name = common.generate_combined_field_name(fieldnames)

		# check instance
		if not isinstance(pseudonym_table, PseudonymTable.PseudonymTable):
			return Logger.log_instance_error('pseudonym_table', 'PseudonymTable')

		# build pseudonym table
		if pseudonym_table is None:
			pseudonym_table = self.build_pseudonym_table(fieldnames, readable, new_field_name=new_field_name)
			if pseudonym_table is None:
				return -1
			self.pseudonym_tables[common.generate_dict_key(fieldnames)] = pseudonym_table

		ds: DataSet.DataSet
		for ds in self.datasets:
			ds.combine_fields_to_pseudonym(fieldnames, pseudonym_table)


	# pseudonymizes the given field
	# if Error occurred: return -1
	def pseudonymize_one(self, fieldname, pseudonym_table=None, readable: bool = True):
		if fieldname is None:
			return Logger.log_none_type_error('fieldname')
		# build a pseudonym table if there is no table given
		if pseudonym_table is None:
			pseudonym_table = self.build_pseudonym_table(fieldname, readable)
			if pseudonym_table is None:
				return -1
			self.pseudonym_tables[common.generate_dict_key(fieldname)] = pseudonym_table
		elif isinstance(pseudonym_table, PseudonymTable.PseudonymTable):
			return Logger.log_instance_error('pseudonym_table', 'PseudonymTable')
		# set the pseudonyms in every dataset
		ds: DataSet.DataSet
		for ds in self.datasets:
			ds.set_pseudonym(fieldname, pseudonym_table)


	# builds the pseudonym table from the current table for the given fields
	def build_pseudonym_table(self, fieldnames, readable, new_field_name: str = None) -> PseudonymTable:
		pseudo_table = PseudonymTable.PseudonymTable(readable, fieldnames, new_fieldname=new_field_name)

		# shuffle datasets to prevent pseudonyms in the same order as the read datasets
		shuffled_datasets = self.datasets.copy()
		random.shuffle(shuffled_datasets)

		ret_value = pseudo_table.build_pseudonyms_from_data(shuffled_datasets)
		if ret_value < 0:
			return None

		return pseudo_table


	def __str__(self):
		output = ""
		output += f"Filename: {str(self.filename)}"
		return output


	def long_string(self):
		output = ""
		output += f"Filename: {str(self.filename)}\n"
		output += h.listToString(self.column_names, 'Column names') + '\n'

		for d in self.datasets:
			output += str(d) + '\n'
		return str(output)


	def get_pseudonym_table_from_fieldnames(self, fieldnames: List):
		Logger.log_method(__name__)
		if fieldnames is None:
			return Logger.log_none_type_error('fieldnames')

		key = common.generate_dict_key(fieldnames)
		if key not in self.pseudonym_tables:
			Logger.log_key_not_found_error(str(key))
			return None

		return self.pseudonym_tables[key]