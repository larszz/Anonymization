import csv
import logging as log
import os
from os import DirEntry
from typing import List

import exceptions as ex
import configurations.Configuration_simple as conf
import objects.TableData as td
import values as v
from configurations.ConfigurationXml import ConfigurationXml
from exceptions import Logger


class DataReader:
	tables: List[td.TableData]


	def __init__(self):
		self.tables = []

	def add_table(self, table: td.TableData):
		if table is None:
			return Logger.log_none_type_error('table')
		self.tables.append(table)


	def readFiles(self, directory, verbose=False):


		log.debug("Directory:\t{0}".format(str(directory)))
		# iterate over found files in directory
		files = os.scandir(directory)
		filename: DirEntry
		for filename in files:
			# exclude sub directories from reading
			if not (os.path.isfile(os.path.join(directory, filename))):
				continue
			if not (str(filename.name).endswith('.csv')):
				ex.Logger.log_info_wrong_file_type(filename, '.csv')
				continue

			log.debug(f"Filename:\t{str(directory)}")

			with open(filename, 'r') as file:
				csv_reader = csv.reader(file, delimiter=v.delimiters.csv.PRIMARY, quotechar=v.delimiters.csv.QUOTECHAR)
				tabledata = td.TableData(filename.name)
				i = 0
				try:
					rows = extractLines(csv_reader)

					# set the column names into tabledata object
					tabledata.set_columnnames(rows[0])

					# set the rest of the data
					if tabledata.add_data(rows[1:]) != 1:
						Logger.log_added_with_errors()

					# add tables to the input data
					self.add_table(tabledata)


				except ex.ColumnNameError as cne:
					log.warning(cne.message)
					continue

		if verbose:
			for t in self.tables:
				print(t.long_string())
		else:
			for t in self.tables:
				print(t)

		return self.tables


	def read_xml_conf(self, configuration: ConfigurationXml, verbose=False):
		directory = configuration.input_directory
		self.readFiles(directory, verbose)


def getColumnNames(firstrow):
	try:
		columns: List[str] = str(firstrow).split(v.delimiters.csv.PRIMARY)
		for x in range(len(columns)):
			columns[x] = str(columns[x]).strip()
		return columns
	except:
		return None


def extractLines(reader):
	rows = []
	for r in reader:
		rows.append(r)
	return rows
