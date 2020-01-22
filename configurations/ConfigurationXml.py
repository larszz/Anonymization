from typing import List
from xml.etree.ElementTree import Element

from objects import AnonymizationPattern
from exceptions import Logger
import xml.etree.cElementTree as ET


# stores information about columns which must be anonymized
class ColAnonymConfig(object):
	column_name: str
	pattern: AnonymizationPattern.Pattern = None


	def __init__(self, column_name: str, pattern: AnonymizationPattern.Pattern = None):
		self.column_name = column_name
		self.pattern = pattern


	def set_pattern(self, pattern: AnonymizationPattern.Pattern):
		if self.pattern is None:
			self.pattern = pattern
		else:
			return Logger.log_already_set('pattern')


# stores a table link
class TableLink(object):
	table_name: str
	table_column: str


	def __init__(self, table_name: str = None, table_column: str = None):
		self.table_name = table_name
		self.table_column = table_column


	def set_table_name(self, name: str):
		if name is None:
			return Logger.log_none_type_error('name')
		if self.table_name is not None:
			return Logger.log_already_set('name')
		self.table_name = name


	def set_table_column(self, name: str):
		if name is None:
			return Logger.log_none_type_error('name')
		if self.table_column is not None:
			return Logger.log_already_set('name')
		self.table_column = name


# stores information about columns which must be pseudonymized
class ColPseudonymConfig(object):
	column_names: List[str]
	readable: bool
	new_fieldname: str
	link: TableLink


	def __init__(self, column_names: List[str] = [], readable: bool = True, new_fieldname: str = None,
				 link: TableLink = None):
		if column_names is None:
			Logger.log_none_type_error('columnnames')
			return

		self.column_names = column_names
		self.readable = readable
		self.new_fieldname = new_fieldname
		self.link = link


	def add_column_name(self, cname: str):
		if cname is None:
			return Logger.log_none_type_error('cname')
		self.column_names.append(cname)

	def set_link(self, link: TableLink):
		if link is None:
			return Logger.log_none_type_error('link')
		if self.link is not None:
			return Logger.log_already_set('link')
		self.link = link



# stores whole information about table configuration
class TableConfig(object):
	table_name: str

	anonymize: List[ColAnonymConfig]
	pseudonymize: List[ColPseudonymConfig]


	def __init__(self, table_name: str = None):
		self.table_name = table_name
		self.anonymize = []
		self.pseudonymize = []


# stores the whole configuration
class ConfigurationXml:
	input_directory: str
	output_directory: str

	tables: List[TableConfig]


	def __init__(self):
		pass


	# constructor reads config from xml
	def read_from_xml(self, config_directory_path: str = None):
		# TODO Implement: read config and set all values
		from values import xml_tags as xt

		path = 'configurations/configuration.xml'
		full_path = 'D:\Projects\Anonymization\configurations\configuration.xml'
		tree = ET.parse(full_path)
		configuration = tree.getroot()

		# get input directory
		e_input_dir: List[Element] = configuration.findall(xt.INPUT_DIR)
		# check if exactly one found
		if len(e_input_dir) < 1:
			return Logger.log_not_found_in_xml(xt.INPUT_DIR, True)
		if len(e_input_dir) > 1:
			Logger.log_too_many_found_in_xml(xt.INPUT_DIR, 1, len(e_input_dir))
		self.input_directory = e_input_dir[0].text

		# get output directory
		e_output_dir: List[Element] = configuration.findall(xt.OUTPUT_DIR)
		# check number of found elements
		if len(e_output_dir) < 1:
			return Logger.log_not_found_in_xml(xt.OUTPUT_DIR, True)
		if len(e_output_dir) > 1:
			Logger.log_too_many_found_in_xml(xt.OUTPUT_DIR, 1, len(e_output_dir))
		self.output_directory = e_output_dir[0].text

		# iterate over tables
		e_tables: List[Element] = configuration.findall(xt.TABLE)
		if len(e_tables) < 1:
			return Logger.log_not_found_in_xml(xt.TABLE, True)

		tab: Element
		for tab in e_tables:
			# get table name
			if xt.TABLENAME in tab.attrib:
				a_name = tab.attrib[xt.TABLENAME]
			else:
				Logger.log_not_found_in_xml(xt.TABLENAME, skip=True)
				continue

			t_config = TableConfig(a_name)
			# #########################################################################################
			# ANONYMIZATION COLUMNS ###################################################################
			e_col_anonym: List[Element] = tab.findall(xt.COLUMNS_ANONYM)

			# skip if no entry found
			if len(e_col_anonym) < 1:
				Logger.log_not_found_in_xml(xt.COLUMNS_ANONYM, skip=True)

			else:
				if len(e_col_anonym) > 1:
					Logger.log_too_many_found_in_xml(xt.COLUMNS_ANONYM, 1, len(e_col_anonym))

				to_anonymize = e_col_anonym[0]

				# get all columns
				cols_anonym: List[Element] = to_anonymize.findall(xt.COLUMN)
				if len(cols_anonym) < 1:
					Logger.log_not_found_in_xml(xt.COLUMN)
				else:
					# iterate over all found columns which must by anonymized
					for column_anonym in cols_anonym:
						# get column names
						e_names = column_anonym.findall(xt.NAME)
						if len(e_names) < 1:
							Logger.log_not_found_in_xml('name', skip=True)
							continue
						if len(e_names) > 1:
							Logger.log_too_many_found_in_xml('name', 1, len(e_names))

						# columns object
						col_config = ColAnonymConfig(column_name=e_names[0])

						# get pattern, if one found
						e_patterns = column_anonym.findall(xt.PATTERN)
						if len(e_patterns) > 0:
							if len(e_patterns) > 1:
								Logger.log_too_many_found_in_xml(xt.PATTERN, 1, len(e_patterns))

							PatternConfig = AnonymizationPattern.Pattern()
							pattern: Element = e_patterns[0]

							# front
							e_front: Element = pattern.find(xt.FRONT)
							if e_front is not None:
								PatternConfig.set_chars_front(e_front.text)

							# end
							e_end: Element = pattern.find(xt.END)
							if e_end is not None:
								PatternConfig.set_chars_end(e_end.text)

							# between
							e_between: Element = pattern.find(xt.BETWEEN)
							if e_between is not None:
								PatternConfig.set_between(e_between.text)

							col_config.set_pattern(PatternConfig)

			# #########################################################################################
			# PSEUDONYMIZATION COLUMNS ################################################################
			e_to_pseudonymize: List[Element] = tab.findall(xt.COLUMNS_PSEUDONYM)

			# skip if no entry found
			if len(e_to_pseudonymize) < 1:
				Logger.log_not_found_in_xml(xt.COLUMNS_PSEUDONYM, skip=True)

			else:
				if len(e_to_pseudonymize) > 1:
					Logger.log_too_many_found_in_xml(xt.COLUMNS_PSEUDONYM, 1, len(e_to_pseudonymize))

				to_pseudonymize = e_to_pseudonymize[0]

				# get all columns
				cols_pseudonym: List[Element] = to_pseudonymize.findall(xt.COLUMN)
				if len(cols_pseudonym) < 1:
					Logger.log_not_found_in_xml(xt.COLUMN)
				else:
					# iterate over all found which must by pseudonymized
					e_column_p: Element
					for e_column_p in cols_pseudonym:
						# get column names
						e_names = e_column_p.findall(xt.NAME)
						if len(e_names) < 1:
							Logger.log_not_found_in_xml('name', skip=True)
							continue

						# init pseudonym config
						pseudonym = ColPseudonymConfig()

						# set the names
						n: Element
						for n in e_names:
							pseudonym.add_column_name(n.text)

						# get readable if specified
						if xt.READABLE in e_column_p.attrib:
							pseudonym.readable = e_column_p.attrib[xt.READABLE]

						# get the new fieldname if specified
						e_newfieldnames: List[Element] = e_column_p.findall(xt.NEW_FIELD_NAME)
						if len(e_newfieldnames) > 0:
							if len(e_newfieldnames) > 1:
								Logger.log_too_many_found_in_xml(xt.NEW_FIELD_NAME, 1, len(e_newfieldnames))

							pseudonym.new_fieldname = e_newfieldnames[0].text

						# get a link with its options if specified
						e_links: List[Element] = e_column_p.findall(xt.LINK)
						if len(e_links) > 0:
							if len(e_links) > 1:
								Logger.log_too_many_found_in_xml(xt.LINK, 1, len(e_links))

							link: Element = e_links[0]
							e_linktable = link.find(xt.LINK_TABLE)
							if e_linktable is not None:
								e_linkcolumn = link.find(xt.LINK_FIELD)
								if e_linkcolumn is not None:
									pseudonym.set_link(TableLink(e_linktable, e_linkcolumn))
								else:
									Logger.log_pattern_error(xt.LINK_FIELD)
							else:
								Logger.log_pattern_error(xt.LINK_TABLE)


		pass
