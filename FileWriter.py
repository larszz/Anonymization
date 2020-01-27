import csv

import FileReader
import objects.TableData as td
import values
from configurations.ConfigurationXml import ConfigurationXml, TableConfig
from exceptions import Logger, log
import common as com

class FileWriter:
	config: ConfigurationXml
	reader: FileReader


	def __init__(self, config: ConfigurationXml, reader: FileReader):
		if config is None:
			Logger.log_none_type_error('config', 'FileReader init')
			return
		if reader is None:
			Logger.log_none_type_error('reader', 'FileReader init')
			return
		self.config = config
		self.reader = reader


	def write_data(self):
		log.info('----------------------------------------------------------------------------')
		log.info('----------------------------------------------------------------------------')
		log.info('------------------------------- FILE WRITING -------------------------------')
		# iterate over table config
		tablename: TableConfig
		for tablename in self.config.get_tables():
			table_data: td.TableData = self.reader.get_table_by_name(tablename)
			if table_data is None:
				return -1

			# TODO: FOR TESTING
			with open(f'{self.config.output_directory}\\{com.get_filename_with_time(tablename)}','w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=values.delimiters.csv.PRIMARY, quotechar=values.delimiters.csv.QUOTECHAR)
				datasets = table_data.get_all_data_in_csv()
				writer.writerow(table_data.column_names)
				for i in range(10):
					writer.writerow(datasets[i])

				pass
