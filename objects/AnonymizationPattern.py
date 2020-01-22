from exceptions import Logger

class Pattern:
	chars_front: int
	chars_end: int
	between: int

	mask_char = '*'

	min_length = -1


	def __init__(self, chars_front = 0, chars_end = 0, between = -1):
		self.chars_front = chars_front
		self.chars_end = chars_end
		self.between = between



	def mask_by_pattern(self, plain: str) -> str:
		# check none
		if plain is None:
			return Logger.log_none_type_error('plain')
		if not isinstance(plain, str):
			return Logger.log_instance_error('plain', 'string')

		# check values already set
		if (self.chars_front == 0) & (self.chars_end == 0):
			return Logger.log_not_set_yet('Front- and end-values')

		# check length possible
		if len(plain) < self.get_min_length():
			return Logger.log_word_too_short(plain, self.get_min_length())

		# if between is not set, the real word length is taken
		mask_length = self.between
		if mask_length == -1:
			mask_length = len(plain) - self.chars_front - self.chars_end

		o = plain[:self.chars_front] + (mask_length * self.mask_char) + plain[-self.chars_end:0]
		return o



	def get_min_length(self):
		# if not already set, set the max length
		if self.min_length == -1:
			self.min_length = self.chars_front + self.chars_end
			if self.between >= 0:
				self.min_length += self.between
		return self.min_length