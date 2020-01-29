from typing import List, Dict

from exceptions import log, ErrorValues

from FileReader import DataReader
from exceptions import Logger
from configurations.ConfigurationXml import ConfigurationXml, TableConfig, ColAnonymConfig, ColPseudonymConfig, \
	LinkConfig
from objects.PseudonymTable import PseudonymTable
from objects.TableData import TableData
from FileWriter import FileWriter


# searchs in all tables for the right table and there for the right pseudo table
def search_for_link(link: LinkConfig, all_tables: Dict):
	if link is None:
		Logger.log_none_type_error('link')
		return None
	if all_tables is None:
		Logger.log_none_type_error('all_tables')

	link_table = link.table_name
	link_fields = link.table_columns

	# get table data for link
	if link_table not in all_tables:
		Logger.log_key_not_found_error(link_table, 'all_tables')
		return None

	table_data: TableData = all_tables[link_table]
	return table_data.get_pseudonym_table_from_fieldnames(link_fields)


# iterating over every anonymize configurations and anonymize column if it can be found
def anonymize_data(config: TableConfig, data: TableData):
	# check none
	if config is None:
		return Logger.log_none_type_error('config')
	if data is None:
		return Logger.log_none_type_error('data')

	anonym_config: List[ColAnonymConfig] = config.get_anonymize()
	error_count = 0
	for conf in anonym_config:
		err = data.anonymize_one(conf.column_name, conf.delete, conf.pattern)
		if err > ErrorValues.DEFAULT_ERROR:
			error_count += err


def pyseudonymize_data(config: TableConfig, data: TableData, all_tables: Dict):
	# check none
	if config is None:
		return Logger.log_none_type_error('config')
	if data is None:
		return Logger.log_none_type_error('data')
	if all_tables is None:
		return Logger.log_none_type_error('all_tables')

	pseudonym_config: List[ColPseudonymConfig] = config.get_pseudonymize()
	for conf in pseudonym_config:
		# get linked pseudo table if specified
		pseudonym_table: PseudonymTable = None
		if conf.link is not None:
			pseudonym_table = search_for_link(conf.link, all_tables)

		if len(conf.column_names) == 1:
			data.pseudonymize_one(conf.column_names[0], pseudonym_table)
		elif len(conf.column_names) > 1:
			data.pseudonymize_many(conf.column_names, pseudonym_table, conf.new_fieldname)


def build_pseudonym_tables(config: ConfigurationXml, reader: DataReader):
	# iterate over table_configs
	Logger.log_info_headline1('generate pseudonym tables')
	table_configs: Dict = config.get_tables()
	for tconfig in table_configs.values():
		Logger.log_info_headline2(tconfig.table_name)
		table_data: TableData = reader.get_table_by_name(tconfig.table_name)
		if table_data is None:
			Logger.log_table_not_found(tconfig.table_name)
			continue

		pseudonym_config: List[ColPseudonymConfig] = tconfig.get_pseudonymize()
		for conf in pseudonym_config:
			# if pseudonym field has not link (so the table has to be generated), build that pseudonym table
			if conf.link is None:
				table_data.build_pseudonym_table(conf.column_names, conf.readable, conf.new_fieldname)
	pass


def manipulate_data(config: ConfigurationXml, reader: DataReader):
	# check none
	if config is None:
		return Logger.log_none_type_error('config')
	if reader is None:
		return Logger.log_none_type_error('reader')

	# generate all pseudonym tables before pseudonymization, to be able to reference a table before it has been pseudonymized
	build_pseudonym_tables(config, reader)

	# iterate over every table in config and apply the configured changes
	Logger.log_info_headline1('manipulation')
	table_configs: Dict = config.get_tables()
	for tconfig in table_configs.values():
		table_data: TableData = reader.get_table_by_name(tconfig.table_name)
		Logger.log_info_headline2(tconfig.table_name)

		# if no table found in data, skip that config
		if table_data is None:
			Logger.log_table_not_found(tconfig.table_name)
			continue
		anonymize_data(tconfig, table_data)
		pyseudonymize_data(tconfig, table_data, reader.get_tables())
		pass


def write_data_to_csv(config: ConfigurationXml, reader: DataReader):
	if config is None:
		return Logger.log_none_type_error('config', 'write_data_to_csv')
	if reader is None:
		return Logger.log_none_type_error('reader', 'write_data_to_csv')

	Logger.log_info_headline1('file writing')
	file_writer = FileWriter(config, reader)
	file_writer.write_pseudonym_tables()
	file_writer.write_data()


if __name__ == '__main__':
	# read configuration
	config = ConfigurationXml()
	if config.read_from_xml() > 0:
		# if configuration could be loaded, read data from input directory
		reader = DataReader()
		reader.read_by_xml_config(config)

		manipulate_data(config, reader)

		write_data_to_csv(config, reader)

		pass
