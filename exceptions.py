class NoneTypeError(Exception):

	def __init__(self, variable):
		self.message = 'Variable "' + str(variable) + '" is NoneType!'
