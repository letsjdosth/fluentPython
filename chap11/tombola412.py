import abc

class Tombola(abc.ABC):
	@abc.abstractmethod
	def load(self, iterable):
		"""iterable의 항목을 추가"""

	@abc.abstractmethod
	def pick(self):
		"""무작위로 항목을 하나 제거하고 제거한 대상을 반환
		비어있을때 메소드 실행 시 LookupError	"""

	def loaded(self):
		"""최소 한 개의 항목이 있으면 True, 아니면 False"""
		return bool(self.inspect())

	def inspect(self):
		"""현재 안에 있는 항목들로 구성된 정렬된 튜플을 반환"""
		items=[]
		while True:
			try:
				items.append(self.pick()) #제거하면서 꺼낸다
			except LookupError:
				break
		self.load(items) #검사했다고 다 제거하는건 이상하니 다시 넣자
		#(이런 방식인 이유는 abc의 메소드는 자기 내부 요소(메소드/속성)만 사용해야하기 때문.
		#나중에 구체적으로 컨테이너를 구현하면서, inspect를 더 나은 방식으로 오버라이드 할 수 있음)
		return tuple(sorted(items))
	#(loaded()도 위의 inspect()를 이용하므로, 지금으로서는 비싼 연산임. (다 꺼내보기 때문.)
	#이 또한 나중에 오버라이드 할 수 있음)


