import collections
from random import choice

Card=collections.namedtuple('Card',['rank','suit'])

class FrenchDeck:
	ranks=[str(n) for n in range(2,11)]+list('JQKA')
	suits='spades diamonds clubs hearts'.split()

	def __init__(self):
		self._cards=[Card(rank,suit) for suit in self.suits
									for rank in self.ranks]

	def __len__(self):
		return len(self._cards)

	def __getitem__(self,position):
		return self._cards[position]

beer_card=Card('7','diamonds')
print(beer_card)

deck=FrenchDeck()
#by __len__
print(len(deck))

#by __getitem__
print(deck[0],deck[-1])
print(choice(deck),choice(deck),choice(deck)) #choice도 __getitem__을 이용한다!!
print(deck[:3]) #slice
print(deck[12::13])
for card in deck: #순회가능!
	print(card)
for card in reversed(deck): #역순으로 순회
	print(card)
print(Card('Q','hearts') in deck) #in 연산
print(Card('7','beast') in deck)

suit_values=dict(spades=3,hearts=2,diamonds=1,clubs=0)
def spade_high(card):
	rank_value=FrenchDeck.ranks.index(card.rank)
	return rank_value*len(suit_values)+suit_values[card.suit] #rank(2~10JQKA) 순. rank 안에서는 클로버-다이아몬드-하트-스페이드 순

for card in sorted(deck, key=spade_high): #오름차순. sorted도 __getitem__ 덕분에 가능
	print(card)