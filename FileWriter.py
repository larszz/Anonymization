import csv
import os
import FileReader
import objects.TableData as td
import values
from configurations.ConfigurationXml import ConfigurationXml, TableConfig
from exceptions import Logger, log, ErrorValues
import common as com
from objects.PseudonymTable import PseudonymTable


class FileWriter:
	config: ConfigurationXml
	reader: FileReader

	directory_name: str = ''
	directory_path: str = ''


	def __init__(self, config: ConfigurationXml, reader: FileReader):
		if config is None:
			Logger.log_none_type_error('config', 'FileReader init')
			return
		if reader is None:
			Logger.log_none_type_error('reader', 'FileReader init')
			return
		self.config = config
		self.reader = reader
		self.directory_name = f"{values.Filenames.DATA}_{com.get_current_time()}"
		self.create_output_directory()


	# creats the output directory for the current program run
	def create_output_directory(self):
		try:
			os.mkdir(os.path.join(self.config.output_directory, self.directory_name))
		except OSError:
			log.error(f"Creation of directory '{self.directory_name}' at {self.config.output_directory} failed!")
		else:
			log.info(f"Created directory '{self.directory_name}' at {self.config.output_directory}.")
			self.directory_path = os.path.join(self.config.output_directory, self.directory_name)


	# writes the data stored in the reader to CSV into the created output directory
	def write_data(self):
		Logger.log_info_headline2('WRITE DATA')
		# iterate over table config
		tablename: str
		for tablename in self.config.get_all_tables():
			table_data: td.TableData = self.reader.get_table_by_name(tablename)
			if table_data is None:
				return ErrorValues.NONETYPE

			log.info(f"Write Table Data:\t{tablename}")

			with open(os.path.join(self.directory_path, tablename), 'w',
					  newline='') as file:
				writer = csv.writer(file, delimiter=values.Delimiters.Csv.PRIMARY,
									quotechar=values.Delimiters.Csv.QUOTECHAR)
				datasets = table_data.get_all_data_in_csv()
				writer.writerow(table_data.column_names)
				writer.writerows(datasets)

			log.info("\tFinished.")
			log.info('')


	# writes the pseudonym tables into the created output directory
	def write_pseudonym_tables(self):
		Logger.log_info_headline2('write pseudonym tables')
		pseudonym_directory = os.path.join(self.directory_path, values.Filenames.PSEUDONYM_TABLES)
		# create the pseudonym directory
		try:
			os.mkdir(pseudonym_directory)
		except OSError:
			log.error(
				f"Creation of directory '{values.Filenames.PSEUDONYM_TABLES}' at {self.directory_path} failed!")
			return ErrorValues.DEFAULT_ERROR
		else:
			log.info(f"Created directory '{values.Filenames.PSEUDONYM_TABLES}' at {self.directory_path}.")

		# iterate over every table in table config
		for tablename in self.config.get_all_tables():
			table_data: td.TableData = self.reader.get_table_by_name(tablename)
			if table_data is None:
				return ErrorValues.NONETYPE

			# iterate over each pseudonym table of the config
			for pseudo_table_name in table_data.pseudonym_tables:
				pseudo_table: PseudonymTable = table_data.get_pseudonym_table_from_columnnames(pseudo_table_name)
				pt_rows = pseudo_table.get_csv_lines()

				pseudo_table_filename = com.get_pseudonymtable_filename(pseudo_table.get_new_fieldname())
				log.info(f"Write PseudonymTable: {pseudo_table_filename}")
				file_path = os.path.join(pseudonym_directory, pseudo_table_filename)
				with open(file_path, 'w', newline='') as file:
					writer = csv.writer(file, delimiter=values.Delimiters.Csv.PRIMARY,
										quotechar=values.Delimiters.Csv.QUOTECHAR)
					writer.writerows(pt_rows)
				log.info('\tFinished.')
				log.info('')
