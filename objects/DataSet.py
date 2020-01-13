import logging as log

import exceptions as ex
import helper as h
import values as v



class DataSet:
	values = None



	def add_to_values(self, key, value):
		if key in self.values:
			log.warning(ex.Messages.KEYALREADYUSED.format(key))
			return

		self.values[str(key)] = DataSet.extractEntries(value)
		log.debug(ex.Messages.Debug.VALUE_ADDED_TO_KEY.format(key, value))
		pass



	def replace_value(self, key, value):
		previous = self.values[key]
		self.values[key] = value
		return previous



	def anonymize_by_pattern(self, key, pattern: str = None):
		newvalue = DataSet.get_pattern_value(self.values[key], pattern)

		# change the value of a field by a given pattern
		previous = self.replace_value(key, newvalue)
		return previous



	def anonymize_random(self, key):
		newvalue = h.get_random_colval()

		previous = self.replace_value(key, newvalue)
		return previous



	def combine_fields(self, keys, newfieldname: str):
		previous = {}
		# add the new value to the "previous" dict to make later unpseudonymization possible
		value = h.get_random_colval()
		previous[newfieldname] = value

		# delete the values corresponding to the given keys from the dict
		for k in keys:
			previous[k] = self.values[k]
			self.values.pop(k)

		self.values[newfieldname] = value
		return previous



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
		output = ""
		for v in self.values:
			output += f'{str(self.values[v])},\t'
		return output



	def __init__(self):
		self.values = {}



	def __getitem__(self, item):
		try:
			return self.values[item]
		except KeyError as ke:
			log.error(ke)



	@staticmethod
	def get_pattern_value(value, pattern):
		# TODO
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
