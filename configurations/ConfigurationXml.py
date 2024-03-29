from typing import List, Dict
from xml.etree.ElementTree import Element

from objects import AnonymizationPattern
from exceptions import Logger, log
import xml.etree.cElementTree as ET


# stores information about columns which must be anonymized
class ColAnonymConfig(object):
	column_name: str
	pattern: AnonymizationPattern.Pattern = None
	delete: bool


	def __init__(self, column_name: str, pattern: AnonymizationPattern.Pattern = None, delete: bool = False):
		self.column_name = column_name
		self.pattern = pattern
		self.delete = delete


	def set_pattern(self, pattern: AnonymizationPattern.Pattern):
		if self.pattern is None:
			self.pattern = pattern
		else:
			return Logger.log_already_set('pattern')


	def __str__(self):
		output = f'Column: {self.column_name}; '
		if self.delete:
			output += 'delete data'
		else:
			if self.pattern is None:
				output += "replace by random values"
			else:
				output += str(self.pattern)
		return output


# stores a table link with the linked file and its referenced column
class LinkConfig(object):
	table_name: str
	table_columns: List[str]


	def __init__(self, table_name: str = None, table_columns: List[str] = None):
		self.table_name = table_name
		if table_columns is None:
			self.table_columns = []
		else:
			self.table_columns = table_columns


	def set_table_name(self, name: str):
		if name is None:
			return Logger.log_none_type_error('name')
		if self.table_name is not None:
			return Logger.log_already_set('name')
		self.table_name = name


	def add_table_column(self, name: str):
		if name is None:
			return Logger.log_none_type_error('name')
		if name == '':
			return Logger.log_string_empty('name')
		self.table_columns.append(name)


	def __str__(self):
		return f"{self.table_name} -> {','.join(self.table_columns)}"


# stores information about columns which must be pseudonymized
class ColPseudonymConfig(object):
	column_names: List[str]
	readable: bool
	new_fieldname: str
	link: LinkConfig


	def __init__(self, column_names: List[str] = None, readable: bool = True, new_fieldname: str = None,
				 link: LinkConfig = None):
		if column_names is None:
			self.column_names = []
		else:
			self.column_names = column_names
		self.readable = readable
		self.new_fieldname = new_fieldname
		self.link = link


	def add_column_name(self, cname: str):
		if cname is None:
			return Logger.log_none_type_error('cname')
		self.column_names.append(cname)


	def set_link(self, link: LinkConfig):
		if link is None:
			return Logger.log_none_type_error('link')
		if self.link is not None:
			return Logger.log_already_set('link')
		self.link = link


	def __str__(self):
		output = 'Pseudonymize:\t'
		output += f"Columnnames: {', '.join(self.column_names)}; {'not' if not self.readable else ''} readable; "
		if self.new_fieldname is not None:
			output += f"new name: {self.new_fieldname}; "
		if self.link is not None:
			output += f"Use pseudonyms: {str(self.link)}"
		return output


# stores whole information about table configuration
class TableConfig(object):
	table_name: str

	anonymize: List[ColAnonymConfig]
	pseudonymize: List[ColPseudonymConfig]

	ignore_in_test: List[str]


	def __init__(self, table_name: str = None):
		self.table_name = table_name
		self.anonymize = []
		self.pseudonymize = []
		self.ignore_in_test = []


	###########################################################################################
	# ADDER ###################################################################################
	def add_anonymize(self, new_config: ColAnonymConfig):
		if new_config is None:
			return Logger.log_none_type_error('new_config')
		self.anonymize.append(new_config)


	def add_pseudonymize(self, new_config: ColPseudonymConfig):
		if new_config is None:
			return Logger.log_none_type_error('new_config')
		self.pseudonymize.append(new_config)


	def add_column_to_ignore(self, column_name: str):
		if column_name is None:
			return -1
		self.ignore_in_test.append(str(column_name))


	###########################################################################################
	# GETTER ##################################################################################
	def get_anonymize(self):
		if self.anonymize is None:
			Logger.log_none_type_error('self.anonymize')
			return []
		return self.anonymize


	def get_pseudonymize(self):
		if self.pseudonymize is None:
			Logger.log_none_type_error('self.pseudonymize')
			return []
		return self.pseudonymize


	def info_to_log(self):
		Logger.log_info_headline2(f"Table: {self.table_name}", False)
		for a in self.anonymize:
			log.info(str(a))
		for p in self.pseudonymize:
			log.info(str(p))


# stores the whole information of a read configuration
class ConfigurationXml:
	input_directory: str
	output_directory: str

	tables: Dict


	def __init__(self):
		self.tables = {}
		pass


	# constructor reads config from xml
	def read_from_xml(self, config_directory_path: str = None):
		from values import XmlTags as xt

		Logger.log_info_headline1('configuration reading')

		path = 'configurations/configuration.xml'
		full_path = 'D:\Projects\Anonymization\configurations\configuration.xml'
		tree = ET.parse(path)
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

		###########################################################################################
		# GET ALL TABLES
		e_tables: List[Element] = configuration.findall(xt.TABLE)
		if len(e_tables) < 1:
			return Logger.log_not_found_in_xml(xt.TABLE, True)

		e_table: Element
		for e_table in e_tables:
			# get table name
			if xt.TABLENAME in e_table.attrib:
				a_name = e_table.attrib[xt.TABLENAME]
			else:
				Logger.log_not_found_in_xml(xt.TABLENAME, skip=True)
				continue

			config_table: TableConfig = TableConfig(a_name)

			###########################################################################################
			# ANONYMIZATION COLUMNS ###################################################################
			# get columns_anonym elements (should be exactly one)
			e_col_anonym: List[Element] = e_table.findall(xt.COLUMNS_ANONYM)

			# skip if no entry found
			if len(e_col_anonym) >= 1:
				if len(e_col_anonym) > 1:
					Logger.log_too_many_found_in_xml(xt.COLUMNS_ANONYM, 1, len(e_col_anonym))

				to_anonymize = e_col_anonym[0]

				# get all columns
				cols_anonym: List[Element] = to_anonymize.findall(xt.COLUMN)
				if len(cols_anonym) < 1:
					Logger.log_not_found_in_xml(xt.COLUMN)
				else:
					# iterate over all found columns which must by anonymized
					for e_column_anonym in cols_anonym:
						# get column names
						e_names: List[Element] = e_column_anonym.findall(xt.NAME)
						if len(e_names) < 1:
							continue
						if len(e_names) > 1:
							Logger.log_too_many_found_in_xml('name', 1, len(e_names))

						# columns object
						config_anonym_col = ColAnonymConfig(column_name=e_names[0].text)

						# get delete-boolean
						if xt.DELETE in e_column_anonym.attrib:
							str_delete = e_column_anonym.attrib[xt.DELETE]
							config_anonym_col.delete = (str_delete == 'true')

						# ignore pattern, if delete is True
						if not config_anonym_col.delete:
							# get pattern, if one found
							e_patterns = e_column_anonym.findall(xt.PATTERN)
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

								config_anonym_col.set_pattern(PatternConfig)

						config_table.add_anonymize(config_anonym_col)

			###########################################################################################
			# PSEUDONYMIZATION COLUMNS ################################################################
			e_to_pseudonymize: List[Element] = e_table.findall(xt.COLUMNS_PSEUDONYM)

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
					# iterate over all found column elements which must by pseudonymized
					e_column_p: Element
					for e_column_p in cols_pseudonym:
						# get column names
						e_names = e_column_p.findall(xt.NAME)
						if len(e_names) < 1:
							Logger.log_not_found_in_xml('name', skip=True)
							continue

						# init pseudonym config
						config_pseudonym_col = None
						config_pseudonym_col = ColPseudonymConfig()

						# set the names
						n: Element
						for n in e_names:
							config_pseudonym_col.add_column_name(n.text)

						# get readable if specified
						if xt.READABLE in e_column_p.attrib:
							txt_readable = e_column_p.attrib[xt.READABLE]
							config_pseudonym_col.readable = (False if txt_readable == 'false' else True)

						# get the new columnname if specified
						e_newfieldnames: List[Element] = e_column_p.findall(xt.NEW_FIELD_NAME)
						if len(e_newfieldnames) > 0:
							if len(e_newfieldnames) > 1:
								Logger.log_too_many_found_in_xml(xt.NEW_FIELD_NAME, 1, len(e_newfieldnames))

							config_pseudonym_col.new_fieldname = e_newfieldnames[0].text

						# get a link with its options if specified
						e_links: List[Element] = e_column_p.findall(xt.LINK)
						if len(e_links) > 0:
							if len(e_links) > 1:
								Logger.log_too_many_found_in_xml(xt.LINK, 1, len(e_links))

							e_link: Element = e_links[0]
							e_linktable = e_link.find(xt.LINK_TABLE)
							if e_linktable is not None:
								e_linkcolumns: List[Element] = e_link.findall(xt.LINK_FIELD)
								if e_linkcolumns is not None:
									linkconfig = LinkConfig(e_linktable.text)
									for link_col in e_linkcolumns:
										linkconfig.add_table_column(link_col.text)
									config_pseudonym_col.set_link(linkconfig)
								else:
									Logger.log_pattern_error(xt.LINK_FIELD)
							else:
								Logger.log_pattern_error(xt.LINK_TABLE)

						config_table.add_pseudonymize(config_pseudonym_col)

			###########################################################################################
			### READ IGNORE_IN_TEST ###################################################################
			e_ignore: List[Element] = e_table.findall(xt.IGNORE_IN_TESTS)

			# skip if no entry found
			if len(e_ignore) > 0:
				if len(e_to_pseudonymize) > 1:
					Logger.log_too_many_found_in_xml(xt.IGNORE_IN_TESTS, 1, len(e_ignore))

				# get ignore_in_tests-Element
				to_ignore = e_ignore[0]

				# iterate over all columns given in parent element
				cols_ignore: List[Element] = to_ignore.findall(xt.COLUMN)

				for c in cols_ignore:
					config_table.add_column_to_ignore(c.text)

			self.tables[config_table.table_name] = config_table

		for t in self.tables.values():
			t.info_to_log()
		return 1


	###########################################################################################
	# GETTER ##################################################################################
	def get_all_tables(self) -> Dict:
		if self.tables is None:
			Logger.log_none_type_error('tables')
			return {}
		return self.tables


	def get_table_by_name(self, name: str):
		# check none
		if name is None:
			Logger.log_none_type_error('name')
			return None

		if name in self.get_all_tables():
			Logger.log_key_not_found_error(name, 'XML Configuration')
			return None

		return self.get_all_tables()[name]
