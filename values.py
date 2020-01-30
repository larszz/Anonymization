class conf:
	DIRECTORY = 'directory'
	OUTPUTDIRECTORY = 'output'
	TABLE = 'table'
	PLAIN = 'plain'
	ANONYM = 'anonym'
	PSEUDONYM = 'pseudonym'


class delimiters:
	class csv:
		PRIMARY = ';'
		SECONDARIES = [',', ';']
		QUOTECHAR = '"'
	class files:
		PSEUDOTABLE_DELIMITER = '__'


class xml_tags:
	DELETE = 'delete'
	INPUT_DIR = 'inputdirectory'
	OUTPUT_DIR = 'outputdirectory'
	TABLE = 'table'
	TABLENAME = 'tablename'
	COLUMNS_ANONYM = 'columns_anonym'
	COLUMN = 'column'
	NAME = 'name'
	PATTERN = 'pattern'
	FRONT = 'front'
	END = 'end'
	COLUMNS_PSEUDONYM = 'columns_pseudonym'
	NEW_FIELD_NAME = 'newfieldname'
	READABLE = 'readable'
	BETWEEN = 'between'
	LINK = 'link'
	LINK_TABLE = 'link_table'
	LINK_FIELD = 'link_field'
	IGNORE_IN_TESTS = 'ignore_in_tests'


class filenames:
	DATA = 'Data'
	PSEUDONYM_TABLES = 'PseudonymTables'


class filesuffix:
	CSV = '.csv'