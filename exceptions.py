import logging as log


class Messages:
	NONETYPEERROR = '"{0}" is NoneType!'
	COLUMNNAMEERROR = 'Column names could not be read from file {0}'
	KEYALREADYUSED = 'Key {0} already used!'
	ALREADYSETERROR = '{0} already set!'
	INSTANCEERROR = '{0} is not instance of {1}'
	DATANOTSETERROR = 'Data could not be set.'
	KEY_NOT_FOUND = 'Key {0} not found in Dictionary'





	class Debug:
		VALUE_ADDED_TO_KEY = 'Value "{1}" added to Key "{0}".'


class NoneTypeError(Exception):

	def __init__(self, variablename):
		self.message = Messages.NONETYPEERROR.format(str(variablename))


class ColumnNameError(Exception):

	def __init__(self, filename):
		self.message = Messages.COLUMNNAMEERROR.format(str(filename))



class Logger:

	@staticmethod
	def log_none_type(fieldname: str):
		if fieldname is None:
			return

		log.warning(Messages.NONETYPEERROR.format(fieldname))
		return -1



	@staticmethod
	def log_instance_error(objectname: str, type: str):
		if (objectname is None) or (type is None):
			return Logger.log_none_type("Object or type")


		log.error(Messages.INSTANCEERROR.format(objectname, type))
		return -2



	@staticmethod
	def log_key_not_found_error(key: str):
		if key is None:
			return Logger.log_none_type('key')


		log.warning(Messages.KEY_NOT_FOUND.format(key))
		return -3


	@staticmethod
	def log_not_set_yet(name: str):
		if name is None:
			return Logger.log_none_type('name')

		log.warning('{0} is not set yet!'.format(name))
		return -4

