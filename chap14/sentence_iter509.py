#고전적인 반복자 패턴 구현
#('디자인 패턴'에서 소개된 대로 그대로 구현)
#참고로 이는 파이써닉하진 않음. 파이썬의 관용적인 방법은 아님
#실제로 파이썬에서 개발 시, 절대 이렇게 하지 말 것 (적절한 방법은 _gen이 붙은 파일 참고)

import re
import reprlib

RE_WORD=re.compile(r'\w+')

class Sentence:
	def __init__(self,text):
		self.text=text
		self.words=RE_WORD.findall(text)

	def __repr__(self):
		return 'Sentence(%s)'%reprlib.repr(self.text)

	def __iter__(self):
		return SentenceIterator(self.words)

class SentenceIterator:
	def __init__(self, words):
		self.words=words
		self.index=0

	def __next__(self):
		try:
			word=self.words[self.index]
		except IndexError:
			raise StopIteration()
		self.index +=1
		return word

	def __iter__(self):
		return self

#iterate test
if __name__=='__main__':
	s=Sentence('"The time has come", thw Walrus said,')
	print(repr(s))
	for word in s:
		print(word)
	print(list(s))

