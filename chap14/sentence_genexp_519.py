#generator expression을 이용할 시
#(설명은 generator_expression518.py 참고)

import re
import reprlib


RE_WORD=re.compile(r'\w+')

class Sentence:
	def __init__(self,text):
		self.text=text
		
	def __repr__(self):
		return 'Sentence(%s)'%reprlib.repr(self.text)

	def __iter__(self):
		# #기존 코드
		# for match in RE_WORD.finditer(self.text):
		# 	yield match.group()
		# return
		return (match.group() for match in RE_WORD.finditer(self.text))

#iterate test
if __name__=='__main__':
	s=Sentence('"The time has come", thw Walrus said,')
	print(repr(s))
	for word in s:
		print(word)
	print(list(s))

