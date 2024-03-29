import binascii
import os
from typing import Tuple, Any, List

from datetime import datetime

import values
from exceptions import Logger


# returns a random hex value
def get_random_hex(length=8):
	return str(binascii.b2a_hex(os.urandom(length)))


# returns a random column value for anonymization
def get_random_colval():
	return str(get_random_hex(5))


# generates the matching key value to the given keys
def generate_dict_key(keys) -> tuple:
	# check none
	if keys is None:
		Logger.log_none_type_error('keys')
		return

	if isinstance(keys, tuple):
		return keys
	if not isinstance(keys, list):
		keys = [keys]

	return to_tuple(keys)


# is called recursively, to generate a working dictionary key from a given structure (might be a list or nested lists)
def to_tuple(value):
	if value is None:
		Logger.log_none_type_error('value', 'common.to_tuple')
		return None
	if isinstance(value, tuple):
		return value
	if isinstance(value, list):
		ret_list = []
		for x in value:
			ret_list.append(to_tuple(x))
		return tuple(i for i in ret_list)
	else:
		return str(value)


# generates a field name with the given filenames
def generate_combined_field_name(fieldnames: List[str]):
	if fieldnames is None:
		return Logger.log_none_type_error('columnnames')

	output: str = "gen"
	for fn in fieldnames:
		output += f'_{fn}'
	output = output.replace(' ', '')
	return output


################################################################################
# TIME #########################################################################

def get_current_time() -> str:
	now = datetime.now()
	return now.strftime("%Y-%m-%d_%H-%M-%S")


def get_filename_with_time(filename: str):
	if filename is None:
		Logger.log_none_type_error('filename', 'common.get_filename_with_time')
		return None
	return f"{get_current_time()}__{filename}"


def get_pseudonymtable_filename(filename: str):
	return '' + filename + values.Filesuffix.CSV
