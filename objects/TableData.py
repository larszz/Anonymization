from typing import List, Dict

import common
import helper as h
from objects import DataSet, PseudonymTable, AnonymizationPattern
import random
from exceptions import Logger, ErrorValues, log


class TableData:
	filename: str = None
	column_names: list
	datasets: list

	pseudonym_tables: Dict = {}


	def __init__(self, filename):
		self.datasets = []
		self.filename = filename
		self.column_names = None
		self.pseudonym_tables = {}


	def set_columnnames(self, columnnames: list):
		if not (self.column_names is None):
			return Logger.log_already_set('Columnnames')
		self.column_names = columnnames


	# sets the filename if it is not set yet
	def set_filename(self, filename):
		if not (self.filename is None):
			return Logger.log_already_set('Filename')

		self.filename = filename


	# adds a dataset to the datasets list
	def add_dataset(self, dataset):
		self.datasets.append(dataset)


	# add the given data, separated into a two-dimensional list; generates a dataset from given data and stores it in the datasets list
	def add_data(self, data):
		if self.column_names is None:
			return Logger.log_none_type_error('Columnnames')

		if data is None:
			return Logger.log_none_type_error('Data')

		if not isinstance(data, list):
			return Logger.log_instance_error('Data', 'list')

		# iterate over every data line
		for idxRow in range(len(data)):
			# create new dataset to store the data line values
			dataset = DataSet.DataSet()
			# iterate over every data line column
			for idxCol in range(len(data[idxRow])):
				try:
					dataset.add_to_values(self.column_names[idxCol], data[idxRow][idxCol])
				except IndexError as ie:
					log.warning('{0}\nidxRow: {1}\tidxCol: {2}'.format(ie, str(idxRow), str(idxCol)))
					continue

			self.add_dataset(dataset)

		return 1


	# anonymizes one given column;
	# if pattern is set: tries to change the column value depending on the pattern
	# if no pattern is given, the value will be changed to a random hex number
	def anonymize_one(self, column, delete: bool, pattern: AnonymizationPattern = None):
		if column is None:
			return Logger.log_none_type_error('column')

		Logger.log_info_table_manipulation_started(self.filename, f'Anonymize One ({column})')
		# delete column in every dataset if found
		error_count = 0
		if delete:
			for ds in self.datasets:
				out = ds.delete_column(column)
				if out < 1:
					error_count += 1
			self.remove_columnnames([column])
		else:
			# if column is not deleted: generate a value for column, random or by pattern
			if pattern is None:
				for ds in self.datasets:
					out = ds.set_columnvalue_random(column)
					if out < 1:
						error_count += 1
			else:
				for ds in self.datasets:
					out = ds.set_columnvalue_by_pattern(column, pattern)
					if out < 1:
						error_count += 1

		Logger.log_info_table_manipulation_finished(error_count)
		return error_count


	# combines multiple given fields into one column, representing the previous values by a pseudonym
	# i.e. pseudonymize a city and its plz by one pseudonym
	def pseudonymize_many(self, columnnames: List[str], pseudonym_table=None,
						  new_field_name: str = None):
		# check none
		if columnnames is None:
			return Logger.log_none_type_error('fields')
		if new_field_name is None:
			new_field_name = common.generate_combined_field_name(columnnames)

		Logger.log_info_table_manipulation_started(self.filename, f'Pseudonymize Many ({",".join(columnnames)})')

		# check instance
		if (pseudonym_table is not None) and not isinstance(pseudonym_table, PseudonymTable.PseudonymTable):
			return Logger.log_instance_error('pseudonym_table', 'PseudonymTable')

		# build pseudonym table
		if pseudonym_table is None:
			pseudonym_table = self.get_pseudonym_table_from_fieldnames(columnnames)
			if pseudonym_table is None:
				return -1

		error_count = 0
		ds: DataSet.DataSet
		for ds in self.datasets:
			err = ds.combine_columns_to_pseudonym(columnnames, pseudonym_table)
			if err <= ErrorValues.DEFAULT_ERROR:
				error_count += 1

		# edit filenames in tabledata
		self.remove_columnnames(columnnames)
		self.add_fieldname(new_field_name)

		Logger.log_info_replaced_column_names(self.filename, columnnames, new_field_name)
		Logger.log_info_table_manipulation_finished(error_count)
		return error_count


	# pseudonymizes the given column
	# if Error occurred: return -1
	def pseudonymize_one(self, columnname, pseudonym_table=None):
		if columnname is None:
			return Logger.log_none_type_error('columnname')

		Logger.log_info_table_manipulation_started(self.filename, f'Pseudonymize One ({columnname})')

		# if no pseudonym table is given, try to get own previously (hopefully) generated pseudonym table
		if pseudonym_table is None:
			pseudonym_table = self.get_pseudonym_table_from_fieldnames([columnname])
			if pseudonym_table is None:
				return ErrorValues.NONETYPE
		elif not isinstance(pseudonym_table, PseudonymTable.PseudonymTable):
			return Logger.log_instance_error('pseudonym_table', 'PseudonymTable')

		# set the pseudonyms in every dataset
		error_count = 0
		ds: DataSet.DataSet
		for ds in self.datasets:
			err = ds.set_pseudonym(columnname, pseudonym_table)
			if err < ErrorValues.DEFAULT_ERROR:
				error_count += 1

		Logger.log_info_table_manipulation_finished(error_count)
		return error_count


	# builds the pseudonym table from the current table for the given fields
	def build_pseudonym_table(self, columnnames, readable, new_field_name: str = None) -> PseudonymTable:
		# check if searched columnnames should actually be existing in this table
		log.info(f"Build pseudonym table for: {str(columnnames)}")
		for f in columnnames:
			if f not in self.column_names:
				Logger.log_table_does_not_contain_column(f, self.filename)
				return ErrorValues.DEFAULT_ERROR

		pseudo_table = PseudonymTable.PseudonymTable(readable, columnnames, new_fieldname=new_field_name)

		# shuffle datasets to prevent pseudonyms in the same order as the read datasets
		shuffled_datasets = self.datasets.copy()
		random.shuffle(shuffled_datasets)

		ret_value = pseudo_table.build_pseudonyms_from_data(shuffled_datasets)
		if ret_value < 0:
			return ret_value

		self.pseudonym_tables[common.generate_dict_key(columnnames)] = pseudo_table
		log.info("\tFinished.")
		return 1


	def __str__(self):
		output = ""
		output += f"Filename: {str(self.filename)}"
		return output


	#####################################################################
	# COLUMN NAME HELPERS ###############################################
	def remove_columnnames(self, columnnames: list):
		if columnnames is None:
			return Logger.log_none_type_error('filenames')
		for c in columnnames:
			if c in self.column_names:
				self.column_names.pop(self.column_names.index(c))
		return 1


	def add_fieldname(self, filename: str):
		if filename is None:
			return Logger.log_none_type_error('filename')
		self.column_names.append(filename)
		return 1


	#####################################################################
	# STRINGS ###########################################################
	def long_string(self):
		output = ""
		output += f"Filename: {str(self.filename)}\n"
		output += h.listToString(self.column_names, 'Column names') + '\n'

		for d in self.datasets:
			output += str(d) + '\n'
		return str(output)


	#####################################################################
	# GETTER ############################################################
	# returns the a pseudonym table, specified by the given columnnames
	def get_pseudonym_table_from_fieldnames(self, fieldnames: List):
		if fieldnames is None:
			Logger.log_none_type_error('columnnames')
			return None

		key = common.generate_dict_key(fieldnames)
		if key not in self.pseudonym_tables:
			Logger.log_key_not_found_error(str(key), 'pseudonym_tables', self.filename)
			return None

		return self.pseudonym_tables[key]


	#####################################################################
	# CSV ###############################################################
	def get_all_data_in_csv(self):
		ds: DataSet.DataSet
		rows = []
		for ds in self.datasets:
			rows.append(ds.to_csv(self.column_names))

		return rows


	#####################################################################
	# ANONYMITY TESTS ###################################################
	def get_sorted_datasets(self) -> List:
		retlist = []
		ds: DataSet.DataSet
		for ds in self.datasets:
			retlist.append(ds.get_values_sorted())
		return retlist
