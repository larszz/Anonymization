from typing import List, Dict

import common
import exceptions as ex
import helper as h
import values as v
from objects import PseudonymTable, AnonymizationPattern
from objects.AnonymizationPattern import Pattern


class DataSet:
	values: Dict = None


	def add_to_values(self, key, value):
		if key in self.values:
			return ex.Logger.log_already_in_dictionary(key)

		self.values[str(key)] = DataSet.extract_entries(value)


	# ex.Logger.log_debug_value_added(key, value)



	# replaces the value for given key
	def replace_value(self, key, value):
		self.values[key] = value


	# ------------------------------------------
	# PSEUDONYMIZATION

	# replaces the given values by one pseudonym
	def combine_columns_to_pseudonym(self, fieldnames, pseudonym_table) -> int:
		# check none
		if fieldnames is None:
			ex.Logger.log_none_type_error('columnnames')
			return -1
		if pseudonym_table is None:
			ex.Logger.log_none_type_error('pseudonym_table')
			return -1

		# check instance
		if not isinstance(pseudonym_table, PseudonymTable.PseudonymTable):
			ex.Logger.log_instance_error('pseudonym_table', 'PseudonymTable')
			return -2

		# get pseudonym
		pseudonym = pseudonym_table.get_pseudonym_from_dataset(self)
		if pseudonym is None:
			return -3

		# delete the values
		for k in fieldnames:
			self.values.pop(k)

		self.values[pseudonym_table.get_new_fieldname()] = [pseudonym]
		return 1


	# sets the value for the given column name to the previous generated pseudonym, selected from the given PseudonymTable
	def set_pseudonym(self, fieldname, pseudonym_table):
		# check none
		if fieldname is None:
			ex.Logger.log_none_type_error('columnname')
			return -1
		if pseudonym_table is None:
			ex.Logger.log_none_type_error('pseudonym_table')
			return -1

		# check instance
		if not isinstance(pseudonym_table, PseudonymTable.PseudonymTable):
			ex.Logger.log_instance_error('pseudonym_table', 'PseudonymTable')
			return -2

		# execute
		pseudonym = pseudonym_table.get_pseudonym_from_dataset(self)
		# cancel, if pseudonym has not been found
		if pseudonym is None:
			return -3

		self.replace_value(fieldname, [pseudonym])
		return 1


	# ------------------------------------------
	# ANONYMIZATION

	# sets the value of a column to itself, masked by the given pattern
	def set_columnvalue_by_pattern(self, columnname, pattern: AnonymizationPattern = None):
		if columnname not in self.values:
			return ex.Logger.log_key_not_found_error(columnname, 'self.values', 'DataSet')
		new_value = DataSet.get_pattern_value(self.values[columnname], pattern)
		# change the value of a column by a given pattern
		self.replace_value(columnname, new_value)
		return 1


	# sets the value of a column to a random hex number
	def set_columnvalue_random(self, columnname):
		self.replace_value(columnname, [common.get_random_colval()])


	def delete_column(self, columnname):
		if columnname is None:
			return ex.Logger.log_none_type_error('columnname')
		if columnname not in self.values:
			return ex.Logger.log_key_not_found_error(columnname, 'self.values', 'DataSet')
		self.values.pop(columnname)
		return 1


	# tries to split a given value string into multiple values, depending on the set secondary delimiters
	@staticmethod
	def extract_entries(valuestring):
		for delim in v.delimiters.csv.SECONDARIES:
			values = str(valuestring).split(delim)

			# return split values, if there is more than 1 entry after split
			if len(values) > 1:
				return values

		# if entry could not be split, return the given valuestring as list
		return [valuestring]


	def __str__(self):
		output = ""
		for val in self.values:
			output += f'{str(self.values[val])},\t'
		return output


	def __init__(self):
		self.values = {}


	def __getitem__(self, item):
		try:
			return self.values[item]
		except KeyError as ke:
			ex.log.error(ke)


	# returns a value from the values-dict
	def get_value(self, key=None):
		if key is None:
			ex.Logger.log_none_type_error('key')
			return None

		if key in self.values:
			return self.values[key]
		else:
			ex.Logger.log_key_not_found_error(key, 'DataSet')
			return None


	# changes the value depending on the given pattern,
	# i.e. to show only the first two digits and exchange the rest by stars *
	@staticmethod
	def get_pattern_value(value: str, pattern: Pattern):
		# check none
		if value is None:
			ex.Logger.log_none_type_error('value')
			return -1
		if pattern is None:
			ex.Logger.log_none_type_error('pattern')
			return -1

		return pattern.mask_by_pattern(value)


	#####################################################################
	# CSV ###############################################################
	def to_csv(self, column_order: List) -> str:
		if column_order is None:
			ex.Logger.log_none_type_error('column_order', 'DataSet.to_csv')
			return

		output: list = []
		field: str
		for field in column_order:
			if field in self.values:
				# put lines with multiple values into QUOTECHARS, connected by delimiter
				content = self.values[field]
				if len(content) > 1:
					output.append(v.delimiters.csv.PRIMARY.join(content))
				else:
					output.append(self.values[field][0])
			else:
				# append an empty string if column not found
				output.append('')

		return output


	#####################################################################
	# ANONYMITY TESTS ###################################################
	def get_values_sorted(self):
		out: list = []
		for key in self.values:
			original_val: list = self.values[key]
			copy_val = original_val.copy()
			sorted(copy_val, key=str.lower)
			out.append('--'.join(copy_val))
		return '|'.join(out)
