
class PseudoEntry:
	new_value = None
	old_values = {}


	def __init__(self, new_value = None):
		self.new_value = new_value
		self.old_values = {}


	def set_new_value(self, new_value):
		self.new_value = new_value


	def add_old_value(self, key, value):
		self.old_values[key] = value
