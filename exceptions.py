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
	DEFAULT_ERROR = -1
	NONETYPE = -1
	INSTANCE_ERROR = -2
	KEY_NOT_FOUND = -3
	NOT_SET_YET = -4
	WORD_TOO_SHORT = -5
	ALREADY_SET = -6
	STRING_EMPTY = -7


logging.basicConfig(format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s')
log = logging.getLogger('AnonymLogger')
log.setLevel(level=logging.DEBUG)


class Logger:
	SEPERATOR1: str = '#################################################################################################'
	SEPERATOR2: str = '##################################################################'


	@staticmethod
	def log_none_type_error(fieldname: str, location: str = None):
		if fieldname is None:
			return ErrorValues.NONETYPE

		log.error(f"{fieldname}{'' if location is None else f' at {location}'} is NoneType!")
		return ErrorValues.NONETYPE


	@staticmethod
	def log_method(methodname: str):
		if methodname is None:
			return Logger.log_none_type_error('methodname')
		log.info(f"Method called: {methodname}")


	@staticmethod
	def log_instance_error(objectname: str, type: str):
		if (objectname is None) or (type is None):
			return Logger.log_none_type_error("Object or type")

		log.error(f"{objectname} is not instance of {type}!")
		return ErrorValues.INSTANCE_ERROR


	@staticmethod
	def log_key_not_found_error(key: str, dictionary_name: str = 'dictionary', location: str = ''):
		if key is None:
			return Logger.log_none_type_error('key')

		log.warning(
			f"{key}: Key not found in {dictionary_name}{'' if ((location == '') or (location is None)) else ' at ' + location}!")
		return ErrorValues.KEY_NOT_FOUND


	@staticmethod
	def log_not_set_yet(name: str):
		if name is None:
			return Logger.log_none_type_error('name')

		log.warning(f'{name} is not set yet!')
		return ErrorValues.NOT_SET_YET


	@staticmethod
	def log_word_too_short(name: str, max_length: int, say_skipping: bool = False):
		if name is None:
			return Logger.log_none_type_error('name')

		log.warning(
			f'{name} is too short for the pattern! (min length: {str(max_length)}){"" if not say_skipping else "   Skipping entry."}')
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
		log.debug(line)
		return ErrorValues.DEFAULT_ERROR


	@staticmethod
	def log_too_many_found_in_xml(name: str, should_be: int, actual: int):
		if name is None:
			return Logger.log_none_type_error('name')

		log.info(f"{name} found too often in XML! (should be: {str(should_be)}; is: {str(actual)})\n"
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


	@staticmethod
	def log_string_empty(name: str):
		if name is None:
			return Logger.log_none_type_error('name')
		log.warning(f"String {name} is empty. Skipping")
		return ErrorValues.STRING_EMPTY


	@staticmethod
	def log_info_new_pseudonym_created(key: str, pseudonym: str):
		if key is None:
			return Logger.log_none_type_error('key')
		if pseudonym is None:
			return Logger.log_none_type_error('pseudonym')

		log.info(f"New pseudonym '{pseudonym}' created (key: {key})")


	@staticmethod
	def log_info_table_manipulation_started(tablename: str, manipulation_type: str):
		log.info(f"{tablename}:\t start '{manipulation_type}'")
		return


	@staticmethod
	def log_info_table_manipulation_finished(error_count: int = -1):
		log.info(f"\tFinished.{f' (Incorrect: {error_count})' if (error_count > (-1)) else ''}")
		log.info('')


	@staticmethod
	def log_info_replaced_column_names(tablename: str, old_columns: list, new_column: str):
		log.info(f"Replaced in {tablename}: {','.join(old_columns)}\t by {new_column}")


	@staticmethod
	def log_table_not_found(tablename):
		log.warning(f"Table not found:\t{tablename}")


	@staticmethod
	def log_table_does_not_contain_column(columnname: str, table: str = None):
		log.warning(f"This table{f' ({table})'} does not countain the column '{columnname}'")


	@staticmethod
	def log_info_headline1(headline: str):
		if headline is None:
			return Logger.log_none_type_error('headline')
		log.info('')
		log.info(Logger.SEPERATOR1)
		log.info(Logger.SEPERATOR1)
		log.info(f'####### {headline.upper()}')


	@staticmethod
	def log_info_headline2(headline: str, uppercase: bool = True):
		if headline is None:
			return Logger.log_none_type_error('headline')
		log.info('')
		log.info(Logger.SEPERATOR2)
		if uppercase:
			headline = headline.upper()
		log.info(f'### {headline}')
		return
