from exceptions import Logger


class Pattern:
	chars_front: int
	chars_end: int
	between: int

	mask_char = '*'

	min_length = -1


	def __init__(self, chars_front: int = 0, chars_end: int = 0, between: int = -1):
		self.chars_front = chars_front
		self.chars_end = chars_end
		self.between = between


	def set_chars_front(self, val: int):
		if self.chars_front == 0:
			self.chars_front = val
		else:
			return Logger.log_already_set('chars_front')


	def set_chars_end(self, val: int):
		if self.chars_end == 0:
			self.chars_end = val
		else:
			return Logger.log_already_set('chars_end')


	def set_between(self, val: int):
		if self.between != 0:
			self.between = val
		else:
			return Logger.log_already_set('between')


	def mask_by_pattern(self, plain_list: list) -> list:
		# check none
		if plain_list is None:
			return Logger.log_none_type_error('plain')

		out_list: list = []
		for plain in plain_list:
			# check values already set
			if (self.chars_front == 0) & (self.chars_end == 0):
				Logger.log_not_set_yet('Front- and end-values')
				continue

			# check length possible
			if len(plain) < self.get_min_length():
				Logger.log_word_too_short(plain, self.get_min_length(), True)
				continue

			# if between is not set, the real word length is taken
			mask_length = self.between
			if mask_length == -1:
				mask_length = len(plain) - int(self.chars_front) - int(self.chars_end)

			out_list.append(plain[0:(int(self.chars_front))] + (int(mask_length) * self.mask_char) + plain[-(int(self.chars_end)):])

		return out_list


	def get_min_length(self) -> int:
		# if not already set, set the max length
		if self.min_length == -1:
			self.min_length = int(self.chars_front) + int(self.chars_end)
			if int(self.between) >= 0:
				self.min_length += int(self.between)
		return self.min_length
