import logging as log


class Messages:"""
	NONETYPEERROR = '"{0}" is NoneType!'
	COLUMNNAMEERROR = 'Column names could not be read from file {0}'
	KEYALREADYUSED = 'Key {0} already used!'
	ALREADYSETERROR = '{0} already set!'
	INSTANCEERROR = '{0} is not instance of {1}'
	DATANOTSETERROR = 'Data could not be set.'
	KEY_NOT_FOUND = 'Key {0} not found in Dictionary'
"""




class Debug:
	VALUE_ADDED_TO_KEY = 'Value "{1}" added to Key "{0}".'


class NoneTypeError(Exception):

	def __init__(self, variablename):
		self.message = Messages.NONETYPEERROR.format(str(variablename))


class ColumnNameError(Exception):

	def __init__(self, filename):
		self.message = Messages.COLUMNNAMEERROR.format(str(filename))


class ErrorValues:
	DEFAULT_ERROR = 0
	NONETYPE = -1
	INSTANCE_ERROR = -2
	KEY_NOT_FOUND = -3
	NOT_SET_YET = -4
	WORD_TOO_SHORT = -5
	ALREADY_SET = -6


class Logger:

	@staticmethod
	def log_none_type_error(fieldname: str):
		if fieldname is None:
			return ErrorValues.NONETYPE

		log.error(f"{fieldname} is NoneType!")
		return ErrorValues.NONETYPE



	@staticmethod
	def log_instance_error(objectname: str, type: str):
		if (objectname is None) or (type is None):
			return Logger.log_none_type_error("Object or type")

		log.error(f"{objectname} is not instance of {type}!")

		return ErrorValues.INSTANCE_ERROR



	@staticmethod
	def log_key_not_found_error(key: str):
		if key is None:
			return Logger.log_none_type_error('key')

		log.warning(f"{key}: Key not found in dictionary!")
		return ErrorValues.KEY_NOT_FOUND


	@staticmethod
	def log_not_set_yet(name: str):
		if name is None:
			return Logger.log_none_type_error('name')

		log.warning(f'{name} is not set yet!')
		return ErrorValues.NOT_SET_YET


	@staticmethod
	def log_word_too_short(name: str, max_length: int):
		if name is None:
			return Logger.log_none_type_error('name')

		log.warning(f'{name} is too short for the pattern! (min length: {str(max_length)})')
		return ErrorValues.WORD_TOO_SHORT


	@staticmethod
	def log_already_set(varname: str):
		if varname is None:
			return Logger.log_none_type_error('varname')

		log.warning(f"{varname} already set!")
		return ErrorValues.ALREADY_SET


	@staticmethod
	def log_added_with_errors():
		log.warning("Data was added with errors!")
		return ErrorValues.DEFAULT_ERROR