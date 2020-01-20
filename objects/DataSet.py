import logging as log

import exceptions as ex
import helper as h
import values as v
from objects import PseudoEntry as pe


class DataSet:
	values = None



	def add_to_values(self, key, value):
		if key in self.values:
			log.warning(ex.Messages.KEYALREADYUSED.format(key))
			return

		self.values[str(key)] = DataSet.extract_entries(value)
		log.debug(ex.Messages.Debug.VALUE_ADDED_TO_KEY.format(key, value))
		pass


	# replaces the value for given key
	# returns: the old value
	def replace_value(self, key, value):
		old_val = self.values[key]
		self.values[key] = value
		return old_val


	# sets the value of a field to itself, masked by the given pattern
	def set_fieldvalue_by_pattern(self, key, pattern: str = None):
		new_value = DataSet.get_pattern_value(self.values[key], pattern)
		# change the value of a field by a given pattern
		self.replace_value(key, new_value)


	# sets the value of a field to a random hex number
	def set_fieldvalue_random(self, key):
		new_value = h.get_random_colval()
		pseudo_entry = pe.PseudoEntry(new_value)
		pseudo_entry.add_old_value(self.replace_value(key, new_value))

		self.replace_value(key)

		return pseudo_entry


	# combines the given values as a key
	def combine_fields(self, keys, new_field_name: str):
		# add the new value to the pseudo entry
		value = h.get_random_colval()
		pseudo_entry = pe.PseudoEntry(value)

		# delete the values corresponding to the given keys from the dict
		for k in keys:
			pseudo_entry.add_old_value(k, self.values[k])
			self.values.pop(k)

		self.values[new_field_name] = value
		return pseudo_entry



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
			log.error(ke)





	# returns a value from the values-dict
	def get_value(self, key=None):
		if key is None:
			ex.Logger.log_none_type('key')
			return None

		if key in self.values:
			return self.values[key]
		else:
			ex.Logger.log_key_not_found_error(key)
			return None


	# changes the value depending on the given pattern,
	# i.e. to show only the first two digits and exchange the rest by stars *
	# TODO: implement
	@staticmethod
	def get_pattern_value(value, pattern):
		return value


"""
	@staticmethod
	def get_new_fieldname(keys):
		separator = '_'
		output = ""
		for k in keys:
			output += str(k) + separator
		output = output.rstrip(separator)
		return output
"""
