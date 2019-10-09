#제너레이터의 더 느긋한 버전 구현
#느긋한 구현: 가능한 한 최후의 순간까지 값 생산을 연기 (메모리 낭비 x, 불필요한 처리 x)

import re
import reprlib

RE_WORD=re.compile(r'\w+')

#기존 코드
class Sentence_gen:
	def __init__(self,text):
		self.text=text
		self.words=RE_WORD.findall(text) #<-이걸 미리 다 만들어놓고 리스트에 통으로 넣은다음

	def __repr__(self):
		return 'Sentence(%s)'%reprlib.repr(self.text)

	def __iter__(self):
		for word in self.words:
			yield word #<-하나씩 주고있다. 이것보다 더 나은 방식이 가능
		return

#개선된 코드
class Sentence:
	def __init__(self,text):
		self.text=text
		
	def __repr__(self):
		return 'Sentence(%s)'%reprlib.repr(self.text)

	def __iter__(self):
		for match in RE_WORD.finditer(self.text): #<-re.finditer()는 re.findall()의 느긋한 버전. 호출시마다 다음으로 매칭되는 부분을 찾아 MatchObject를 생성한다
			yield match.group() #MatchObject의 group()은 매칭되는 텍스트를 추출한다
		return
	#__iter__는 호출될때마다 정규식 조건에 맞는 요소를 하나씩 찾아서 yield로 넘긴다.

#iterate test
if __name__=='__main__':
	s=Sentence('"The time has come", thw Walrus said,')
	print(repr(s))
	for word in s:
		print(word)
	print(list(s))

