from typing import List
from xml.etree.ElementTree import Element

from objects import AnonymizationPattern
from exceptions import Logger
import xml.etree.cElementTree as ET


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
class TableConfiguration(object):
	table_name: str

	anonymize: List[ColumnAnonym]
	pseudonymize: List[ColumnPseudonym]


	def __init__(self):
		pass


class Configuration_XML:
	input_directory: str
	output_directory: str

	tables: List[TableConfiguration]

	def __init__(self):
		pass

	# constructor reads config from xml
	def read_from_xml(self, config_directory_path: str = None):
		# TODO Implement: read config and set all values
		from values import xml_names as xn

		path = 'configurations/configuration.xml'
		full_path = 'D:\Projects\Anonymization\configurations\configuration.xml'
		tree = ET.parse(full_path)
		configuration = tree.getroot()

		# get input directory
		e_input_dir: List[Element] = configuration.findall(xn.INPUT_DIR)
		# check if exactly one found
		if len(e_input_dir) < 1:
			return Logger.log_not_found_in_xml(xn.INPUT_DIR, True)
		if len(e_input_dir) > 1:
			Logger.log_too_many_found_in_xml(xn.INPUT_DIR, 1, len(e_input_dir))
		self.input_directory = e_input_dir[0].text


		# get output directory
		e_output_dir: List[Element] = configuration.findall(xn.OUTPUT_DIR)
		# check number of found elements
		if len(e_output_dir) < 1:
			return Logger.log_not_found_in_xml(xn.OUTPUT_DIR, True)
		if len(e_output_dir) > 1:
			Logger.log_too_many_found_in_xml(xn.OUTPUT_DIR, 1, len(e_output_dir))
		self.output_directory = e_output_dir[0].text

		# iterate over tables



		pass
