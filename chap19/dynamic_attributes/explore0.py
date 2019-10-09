#목표 : JS처럼, json을 dict가 아니라 점 표기법으로 읽을 수 있도록 하자

from collections import abc

class FrozenJson:
	"""점 표기법을 이용해 JSON과 유사한 객체를 순회하는 읽기 전용 퍼사드 클래스"""
	def __init__(self, mapping):
		self.__data=dict(mapping) #dict 사본

	def __getattr__(self, name):
		if hasattr(self.__data, name):
			return getattr(self.__data, name)
		else:
			try:
				return FrozenJson.build(self.__data[name])
			except KeyError as exc:
				raise AttributeError('no "{}" attribute in this mapping'.format(name)) from exc

	@classmethod
	def build(cls, obj):
		if isinstance(obj, abc.Mapping): #dict류
			return cls(obj)
		elif isinstance(obj, abc.MutableSequence): #list류
			return [cls.build(item) for item in obj]
		else:
			return obj

#for test
if __name__=='__main__':
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