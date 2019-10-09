#파이써닉하게 반복자 구현

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
		#iterator class(반복자 클래스) 대신 제너레이터 함수를 쓰자
		for word in self.words:
			yield word
		return


#iterate test
if __name__=='__main__':
	s=Sentence('"The time has come", thw Walrus said,')
	print(repr(s))
	for word in s:
		print(word)
	print(list(s))

