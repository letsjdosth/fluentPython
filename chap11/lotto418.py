import random

from tombola412 import Tombola


class LotteryBlower(Tombola):
	def __init__(self,iterable):
		self._balls=list(iterable)

	def load(self, iterable):
		self._balls.extend(iterable)

	def pick(self):
		try:
			position=random.randrange(len(self._balls)) #범위가 비면 randrange()는 ValueError를 낸다
		except ValueError:
			raise LookupError('pick from empty BingoCage')
		return self._balls.pop(position)

	def loaded(self): #상속된 loaded보다 더 낫게 override하자
		return bool(self._balls)

	def inspect(self): #마찬가지로 override하자
		return tuple(sorted(self._balls))