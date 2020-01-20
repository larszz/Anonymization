import binascii
import os
from typing import Tuple, Any

from exceptions import Logger


def get_random_hex(length=8):
	return str(binascii.b2a_hex(os.urandom(length)))


def get_random_colval():
	return str(get_random_hex(5))


# generates the matching key value to the given keys
def generate_dict_key(keys) -> tuple:
	# check none
	if keys is None:
		Logger.log_none_type('keys')
		return

	# if keys are already a tuple, return that tuple
	if not isinstance(keys, tuple):
		# keys are a list
		if isinstance(keys, list):
			return tuple(str(i) for i in keys)
		# keys is actually only one key
		else:
			t: Tuple[Any] = (str(keys),)
			return t
	return keys
