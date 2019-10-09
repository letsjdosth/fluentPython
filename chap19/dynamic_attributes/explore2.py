#목표 : JS처럼, json을 dict가 아니라 점 표기법으로 읽을 수 있도록 하자
#목표 v1: json 항목명이 파이썬 예약어와 겹치는 경우/적절한 어트리뷰트 명이 아닌 경우에 대처하자
#목표 v2: __new__를 이용한 개선 (p714)

from collections import abc
import keyword

class FrozenJson:
	"""점 표기법을 이용해 JSON과 유사한 객체를 순회하는 읽기 전용 퍼사드 클래스"""
	def __new__(cls,arg): #<-실제로는 클래스메소드이다. 객체 생성시 이를 호출한다. 첫 인자는 클래스 자신이다. #기존 build를 대체한다.
		if isinstance(arg, abc.Mapping):
			return super().__new__(cls) #<-object.__new__(FrozenJson) 을 호출한다. 기본적으로는 object에 위임하는 방식으로 만든다.
		elif isinstance(arg, abc.MutableSequence):
			return [cls(item) for item in arg]
		else:
			return arg

	def __init__(self, mapping):
		self.__data={}
		for key, value in mapping.items():
			if keyword.iskeyword(key): #예약어이면
				key+='_'
			if not key.isidentifier(): #파이썬 규칙상 부적합한 이름이면
				key='_'+key
			self.__data[key]=value

	def __getattr__(self, name):
		if hasattr(self.__data, name):
			return getattr(self.__data, name)
		else:
			try:
				return FrozenJson.build(self.__data[name])
			except KeyError as exc:
				raise AttributeError('no "{}" attribute in this mapping'.format(name)) from exc



#for test
if __name__=='__main__':
	#v0 test
	from osconfeed707 import load
	raw_feed=load() #json 모듈을 이용해 dict로 가져온다
	feed=FrozenJson(raw_feed)

	print(len(feed.Schedule.speakers)) #357 #<-점 표기법 접근. 그 뿐 아니라 getattr이 제공하는 요소들을 모두 쓸 수 있다(key/items/len...)
	print(sorted(feed.Schedule.keys())) #['conferences', 'events', 'speakers', 'venues']
	for key,value in sorted(feed.Schedule.items()):
		print('{:3} {}'.format(len(value), key))
	print(feed.Schedule.speakers[-1].name) #Carina C. Zona

	talk=feed.Schedule.events[40]
	print(type(talk),talk.name,talk.speakers) #<class '__main__.FrozenJson'> There *Will* Be Bugs [3471, 5199]
	try:
		print(talk.flavor) #talk에 flaver라는건 없다..
	except AttributeError:
		pass

	#v1 test
	grad=FrozenJson({'name':'Jim Bo','class':1982, '2be':'or not'})
	# print(grad.class) #SyntaxError: invalid syntax
	print(grad.class_) #1982
	# print(grad.2be) #SyntaxError: invalid syntax
	print(grad._2be) #or not