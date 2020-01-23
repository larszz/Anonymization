import logging


class Messages: """
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


logging.basicConfig(format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s')
log = logging.getLogger('AnonymLogger')
log.setLevel(level=logging.DEBUG)


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


	@staticmethod
	def log_not_found_in_xml(name: str, exit=False, skip=False):
		if name is None:
			return Logger.log_none_type_error('name')
		line = f"No {name} found in XML!"
		if exit:
			line += " Exiting."
		if skip:
			line += " Skipping."
		log.warning(line)
		return ErrorValues.DEFAULT_ERROR


	@staticmethod
	def log_too_many_found_in_xml(name: str, should_be: int, actual: int):
		if name is None:
			return Logger.log_none_type_error('name')

		log.warning(f"{name} found too often in XML! (should be: {str(should_be)}; is: {str(actual)})\n"
					f"Continue with first found element.")
		return ErrorValues.DEFAULT_ERROR


	@staticmethod
	def log_pattern_error(element_not_found: str):
		if element_not_found is None:
			return Logger.log_none_type_error('element_not_found')

		log.warning(f"Element '{element_not_found}' not set. Skipping pattern.")
		return ErrorValues.DEFAULT_ERROR


	@staticmethod
	def log_already_in_dictionary(key: str):
		if key is None:
			return Logger.log_none_type_error('key')
		log.warning(f"Key '{key}' already in dictionary!")
		return ErrorValues.ALREADY_SET


	@staticmethod
	def log_debug_value_added(key: str, value: str):
		if key is None:
			return Logger.log_none_type_error('key')
		if value is None:
			return Logger.log_none_type_error('value')
		log.debug(f"Added to dictionary: {key} -> {value}")


	@staticmethod
	def log_info_wrong_file_type(filename: str, should_be: str):
		if filename is None:
			return Logger.log_none_type_error('filename')
		if should_be is None:
			return Logger.log_none_type_error('should_be')
		log.info(f"File '{filename}' is skipped due to wrong file type. (should be: {should_be})")