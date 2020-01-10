import os
from typing import List
import exceptions as ex
import helper as h
import objects as o
import logging as log
import csv
import values as v

log.basicConfig(format='%(asctime)s %(message)s')


def readFile(configuration):
	tables = []

	# check object types
	if not isinstance(configuration, o.Configuration):
		return -1

	# iterate over given directories
	for directory in configuration.file_directories:
		log.info("Directory:\t{0}".format(str(directory)))
		# iterate over found files in directory
		files = os.scandir(directory)
		for filename in files:
			# exclude sub directories from reading
			if not (os.path.isfile(os.path.join(directory, filename))):
				continue

			log.info("Filename:\t{0}".format(str(directory)))

			with open(filename, 'r') as file:
				csv_reader = csv.reader(file, delimiter=v.delimiters.csv.PRIMARY, quotechar=v.delimiters.csv.QUOTECHAR)

				tabledata = o.TableData(filename)
				i = 0
				try:
					rows = extractLines(csv_reader)

					# set the column names into tabledata object
					tabledata.set_columnnames(rows[0])

					# set the rest of the data
					if tabledata.add_data(rows[1:]) != 1:
						log.error(ex.Messages.DATANOTSETERROR)

					# add tables to the input data
					tables.append(tabledata)




				except ex.ColumnNameError as cne:
					log.warning(cne.message)
					continue

	for t in tables:
		print(t)

	return tables


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
