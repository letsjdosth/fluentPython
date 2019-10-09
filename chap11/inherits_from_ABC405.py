import collections

Card=collections.namedtuple('Card',['rank','suit'])

'''
https://docs.python.org/3/library/collections.abc.html
Sequence
|Inherits from: Reversible, Collection
|Abstriact methods: __getitem__, __len__ #<-상속 시 무조건 구현해야 함!
|Mixin Methods: __contains__, __iter__, __reversed__, index, and count #<-위가 구현되면 파이썬 인터프리터가 이를 알아서 지원!
|
MutableSequence
Abstract Method: __getitem__, __setitem__, __delitem__, __len__, insert #<-상속 시 무조건 구현해야 함!
Mixin Methods: Inherited Sequence methods and append, reverse, extend, pop, remove, and __iadd__ #<-위가 구현되면 파이썬 인터프리터가 이를 알아서 지원!
'''

class FrenchDeck2(collections.MutableSequence):
	ranks=[str(n) for n in range(2,11)]+list('JQKA')
	suits='spades diamonds clubs hearts'.split()

	def __init__(self):
		self._cards=[Card(rank,suit) for suit in self.suits for rank in self.ranks]

	def __len__(self):
		return len(self._cards)

	def __getitem__(self,position):
		return self._card[position]

	def __setitem__(self,position,value):
		self._cards[position]=value

	def __delitem__(self,position):
		del self._cards[position]

	def insert(self, position, value):
		self._cards.insert(position, value)
