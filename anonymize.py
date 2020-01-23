from typing import List, Dict

from exceptions import log

from FileReader import DataReader
from exceptions import Logger
from configurations.ConfigurationXml import ConfigurationXml, TableConfig, ColAnonymConfig, ColPseudonymConfig, \
	LinkConfig
from objects.PseudonymTable import PseudonymTable
from objects.TableData import TableData


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
	Logger.log_method(__name__)
	# check none
	if config is None:
		return Logger.log_none_type_error('config')
	if data is None:
		return Logger.log_none_type_error('data')

	anonym_config: List[ColAnonymConfig] = config.get_anonymize()
	for conf in anonym_config:
		data.anonymize_one(conf.column_name, conf.pattern)



def pyseudonymize_data(config: TableConfig, data: TableData, all_tables: Dict):
	Logger.log_method(__name__)
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
		pseudonym_table: PseudonymTable = search_for_link(conf.link, all_tables)

		if len(conf.column_names) == 1:
			data.pseudonymize_one(conf.column_names[0], pseudonym_table, conf.readable)
		elif len(conf.column_names) > 1:
			data.pseudonymize_many(conf.column_names, pseudonym_table, conf.readable, conf.new_fieldname)







#
def manipulate_data(config: ConfigurationXml, reader: DataReader):
	# check none
	if config is None:
		return Logger.log_none_type_error('config')
	if reader is None:
		return Logger.log_none_type_error('reader')

	# iterate over every table in config
	table_configs: Dict = config.get_tables()
	for tconfig in table_configs.values():
		table_data: TableData = reader.get_table_by_name(tconfig.table_name)
		# if no table found in data, skip that config
		if table_data is None:
			continue

		anonymize_data(tconfig, table_data)
		pyseudonymize_data(tconfig, table_data, reader.get_tables())
		pass




if __name__ == '__main__':
	# read configuration
	config = ConfigurationXml()
	if config.read_from_xml() > 0:
		# if configuration could be loaded, read data from input directory
		reader = DataReader()
		reader.read_by_xml_config(config)

		manipulate_data(config, reader)
