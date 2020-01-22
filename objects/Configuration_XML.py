from typing import List
from objects import AnonymizationPattern
from exceptions import Logger


class Configuration_XML:
	input_directory: str
	output_directory: str


	# constructor
	def __init__(self):
		pass


# stores information about columns which must be anonymized
class ColumnAnonym(object):
	column_name: str
	pattern: AnonymizationPattern.Pattern = None


	def __init__(self, column_name: str, pattern: AnonymizationPattern.Pattern = None):
		self.column_name = column_name
		self.pattern = pattern


# stores a table link
class TableLink(object):
	table_name: str
	table_column: str


	def __init__(self, table_name: str, table_column: str):
		self.table_name = table_name
		self.table_column = table_column


# stores information about columns which must be pseudonymized
class ColumnPseudonym(object):
	column_names: List[str]
	readable: bool
	new_fieldname: str
	link: TableLink


	def __init__(self, columnnames: List[str], readable: bool = True, new_fieldname: str = None,
				 link: TableLink = None):
		if columnnames is None:
			Logger.log_none_type_error('columnnames')
			return

		self.column_names = columnnames
		self.readable = readable
		self.new_fieldname = new_fieldname
		self.link = link


# stores whole information about table configuration
class TableConfiguration:
	table_name: str

	anonymize: List[ColumnAnonym]
	pseudonymize: List[ColumnPseudonym]


	def __init__(self):
		pass
