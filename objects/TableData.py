import logging as log

import exceptions as ex
import helper as h
import objects.DataSet as ds



class TableData:
	filename = None
	column_names = None
	datasets: dict



	def __init__(self, filename):
		self.datasets = []
		self.filename = filename



	def set_columnnames(self, columnnames):
		if not (self.column_names is None):
			log.error(ex.Messages.ALREADYSETERROR.format('Columnnames'))
			return -1
		self.column_names = columnnames



	def set_filename(self, filename):
		if not (self.filename is None):
			log.error(ex.Messages.ALREADYSETERROR.format('Filename'))
			return -1

		self.filename = filename



	def add_dataset(self, dataset):
		self.datasets.append(dataset)



	def add_data(self, data):
		if self.column_names is None:
			log.error(ex.Messages.NONETYPEERROR.format('Columnnames'))
			return -1

		if data is None:
			log.error(ex.Messages.NONETYPEERROR.format('Data'))
			return -1

		if not isinstance(data, list):
			log.error(ex.Messages.INSTANCEERROR.format('Data', 'List'))
			return -1

		for idxRow in range(len(data)):
			dataset = ds.DataSet()
			for idxCol in range(len(data[idxRow])):
				try:
					dataset.add_to_values(self.column_names[idxCol], data[idxRow][idxCol])
				except IndexError as ie:
					log.warning('Error: {0}\nidxRow: {1}\tidxCol: {2}'.format(ie.message, str(idxRow), str(idxCol)))
					continue

			self.add_dataset(dataset)

		return 1



	def anonymize_one(self, field, pattern=None):
		for ds in self.datasets:
			ds.anonymize_by_pattern(field, pattern)



	def pseudonymize_many(self, fields, newfieldname: str = None):
		for ds in self.datasets:
			ds.combine_fields(fields, newfieldname)



	def __str__(self):
		output = ""
		output += f"Filename: {str(self.filename)}\n"
		output += h.listToString(self.column_names, 'Column names') + '\n'

		for d in self.datasets:
			output += str(d) + '\n'
		return str(output)
