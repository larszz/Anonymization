class Messages:
	NONETYPEERROR = '"{0}" is NoneType!'
	COLUMNNAMEERROR = 'Column names could not be read from file {0}'


class NoneTypeError(Exception):

	def __init__(self, variablename):
		self.message = Messages.NONETYPEERROR.format(str(variablename))


class ColumnNameError(Exception):
	def __init__(self, filename):
		self.message = Messages.COLUMNNAMEERROR.format(str(filename))
