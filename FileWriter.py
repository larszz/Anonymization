import csv
import os
import FileReader
import objects.TableData as td
import values
from configurations.ConfigurationXml import ConfigurationXml, TableConfig
from exceptions import Logger, log
import common as com

class FileWriter:
	config: ConfigurationXml
	reader: FileReader

	directory_name: str = ''

	def __init__(self, config: ConfigurationXml, reader: FileReader):
		if config is None:
			Logger.log_none_type_error('config', 'FileReader init')
			return
		if reader is None:
			Logger.log_none_type_error('reader', 'FileReader init')
			return
		self.config = config
		self.reader = reader
		self.directory_name = f"{values.filenames.DATA}_{com.get_current_time()}"


	def write_data(self):
		Logger.log_info_headline1('file writing')

		# create directory with current date to store the generated information in

		try:
			os.mkdir(os.path.join(self.config.output_directory, self.directory_name))
		except OSError:
			log.error(f"Creation of directory '{self.directory_name}' at {self.config.output_directory} failed!")
		else:
			log.info(f"Created directory '{self.directory_name}' at {self.config.output_directory}.")


		# iterate over table config
		tablename: str
		for tablename in self.config.get_tables():
			log.info(f"Write Table:\t{tablename}")
			table_data: td.TableData = self.reader.get_table_by_name(tablename)
			if table_data is None:
				return -1

			with open(os.path.join(self.config.output_directory, self.directory_name, tablename),'w', newline='') as file:
				writer = csv.writer(file, delimiter=values.delimiters.csv.PRIMARY, quotechar=values.delimiters.csv.QUOTECHAR)
				datasets = table_data.get_all_data_in_csv()
				writer.writerow(table_data.column_names)
				for i in range(10):
					writer.writerow(datasets[i])

			log.info("\tFinished.")
