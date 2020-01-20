import logging as log

class Messages:
	NONETYPEERROR = '"{0}" is NoneType!'
	COLUMNNAMEERROR = 'Column names could not be read from file {0}'
	KEYALREADYUSED = 'Key {0} already used!'
	ALREADYSETERROR = '{0} already set!'
	INSTANCEERROR = '{0} is not instance of {1}'
	DATANOTSETERROR = 'Data could not be set.'





	class Debug:
		VALUE_ADDED_TO_KEY = 'Value "{1}" added to Key "{0}".'


class NoneTypeError(Exception):

	def __init__(self, variablename):
		self.message = Messages.NONETYPEERROR.format(str(variablename))


class ColumnNameError(Exception):

	def __init__(self, filename):
		self.message = Messages.COLUMNNAMEERROR.format(str(filename))



class Logger:
	def log_none_type(self, fieldname: str=None):
		if fieldname is None:
			return

		log.warning(Messages.NONETYPEERROR.format(fieldname))


	def log_instance_error(self, obj: str=None, type: str=None):
		if (obj is None) or (type is None):
			self.log_none_type("Object or type")
			return

		log.error(Messages.INSTANCEERROR.format(objectname, type))

