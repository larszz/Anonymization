import logging as log

import common
import exceptions as ex
import helper as h
from objects import DataSet, PseudonymTable
import random


class TableData:
	filename = None
	column_names = None
	datasets: dict

	pseudonym_tables = {}



	def __init__(self, filename):
		self.datasets = []
		self.filename = filename



	def set_columnnames(self, columnnames):
		if not (self.column_names is None):
			log.error(ex.Messages.ALREADYSETERROR.format('Columnnames'))
			return -1
		self.column_names = columnnames



	def set_filename(self, filename):
		if not (self.filename is None):
			log.error(ex.Messages.ALREADYSETERROR.format('Filename'))
			return -1

		self.filename = filename



	def add_dataset(self, dataset):
		self.datasets.append(dataset)



	# add the given data, separated into a two-dimensional list
	def add_data(self, data):
		if self.column_names is None:
			ex.Logger.log_none_type('Columnnames')
			return -1

		if data is None:
			ex.Logger.log_none_type('Data')
			return -1

		if not isinstance(data, list):
			log.error(ex.Messages.INSTANCEERROR.format('Data', 'List'))
			return -1

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
	def pseudonymize_many(self, fieldnames, pseudonym_table=None, readable: bool = False,
						  newfieldname: str = None):
		# check none
		if fieldnames is None:
			ex.Logger.log_none_type('fields')
			return -1
		if pseudonym_table is None:
			ex.Logger.log_none_type('pseudonym_table')
			return -1
		if newfieldname is None:
			ex.Logger.log_none_type('newfieldname')
			return -1

		# check instance
		if not isinstance(pseudonym_table, PseudonymTable.PseudonymTable):
			ex.Logger.log_instance_error('pseudonym_table', 'PseudonymTable')
			return -2

		# build pseudonym table
		if pseudonym_table is None:
			pseudonym_table = self.build_pseudonym_table(fieldnames, readable)
			if pseudonym_table is None:
				return -1
			self.pseudonym_tables[common.generate_dict_key(fieldnames)] = pseudonym_table

		ds: DataSet.DataSet
		for ds in self.datasets:
			ds.combine_fields_to_pseudonym(fieldnames, pseudonym_table)





	# pseudonymizes the given field
	# if Error occurred: return -1
	def pseudonymize_one(self, fieldname, pseudonym_table=None, readable: bool = True):
		# build a pseudonym table if there is no table given
		if pseudonym_table is None:
			pseudonym_table = self.build_pseudonym_table(fieldname, readable)
			if pseudonym_table is None:
				return -1
			self.pseudonym_tables[common.generate_dict_key(fieldname)] = pseudonym_table

		# set the pseudonyms in every dataset
		ds: DataSet.DataSet
		for ds in self.datasets:
			ds.set_pseudonym(fieldname, pseudonym_table)



	# builds the pseudonym table from the current table for the given fields
	def build_pseudonym_table(self, fieldnames, readable) -> PseudonymTable:
		pseudo_table = PseudonymTable.PseudonymTable(readable, fieldnames)

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
