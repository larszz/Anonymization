import FileReader
from configurations.ConfigurationXml import ConfigurationXml, TableConfig
from exceptions import Logger
from objects.TableData import TableData


def k_anonymity(config: ConfigurationXml, reader: FileReader):
	if config is None:
		return Logger.log_none_type_error('config')
	if reader is None:
		return Logger.log_none_type_error('reader')

	# iterate over every table config
	tconfig: TableConfig
	for tconfig in config.get_tables().values():
		table_data: TableData = reader.get_table_by_name(tconfig.table_name)
		if table_data is None:
			Logger.log_table_not_found(tconfig.table_name)
			continue

		ds_list = table_data.get_test_data(tconfig.ignore_in_test)

		# count the dataset values in dictionary
		counting_dict: dict[str, int] = {}
		ds: str
		for ds in ds_list:
			if ds in counting_dict:
				counting_dict[ds] = int(counting_dict[ds]) + 1
			else:
				counting_dict[ds] = 1

		k_value = min(counting_dict.values())
		Logger.log_k_anonymity(tconfig.table_name, k_value, tconfig.ignore_in_test)
		pass



