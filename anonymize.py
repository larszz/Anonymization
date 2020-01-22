
import logging as log

from FileReader import DataReader
from exceptions import Logger
from configurations.ConfigurationXml import ConfigurationXml

if __name__ == '__main__':
	# read configuration
	config = ConfigurationXml()
	if config.read_from_xml() >0:
		reader = DataReader()
		reader.read_xml_conf(config, False)

