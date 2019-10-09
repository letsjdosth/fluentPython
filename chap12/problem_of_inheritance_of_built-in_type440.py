#CPython에서 C로 짜여진 부분에 있어서는, 해당 클래스를 파이썬 내에서 상속받아 메서드를 오버라이드해도 동작하지 않는다

#예1
class DoppelDict(dict):
	def __setitem__(self,key,value):
		super().__setitem__(key,[value]*2)

dd=DoppelDict(one=1)
print(dd) #{'one': 1} #<-{'one': [1, 1]}이 아니다! dict의 __init__이 __setitem__의 오버라이드를 무시해버렸다..

dd['two']=2
print(dd) #{'one': 1, 'two': [2, 2]} #<-[]는 오버라이드된 __setitem__을 호출하였다

dd.update(three=3)
print(dd) #{'one': 1, 'two': [2, 2], 'three': 3} #<-update는 또 무시하였다...


#예2 (Pypy의 예)
class AnswerDict(dict):
	def __getitem__(self, key):
		return 42

ad=AnswerDict(a='foo')
print(ad['a']) #42

d={}
d.update(ad)
print(d['a']) #foo #<-오버라이드된 __getitem__을 무시하고 가져왔다
print(d) #{'a': 'foo'}




#기본 자료형 상속시엔 내장자료형을 직접 상속하지 말고, collection module에서 상속용 User~를 사용하는 것이 좋음
import collections

#예1 수정판
class DoppelDict(collections.UserDict):
	def __setitem__(self,key,value):
		super().__setitem__(key,[value]*2)

dd=DoppelDict(one=1)
print(dd) #{'one': [1, 1]}

dd['two']=2
print(dd) #{'one': [1, 1], 'two': [2, 2]}

dd.update(three=3)
print(dd) #{'one': [1, 1], 'two': [2, 2], 'three': [3, 3]} #모두 일관성 있게 오버라이드 된 메소드로 작동한다


#예2 수정판
class AnswerDict(collections.UserDict):
	def __getitem__(self, key):
		return 42

ad=AnswerDict(a='foo')
print(ad['a']) #42

d={}
d.update(ad)
print(d['a']) #42
print(d) #{'a': 42} #마찬가지로 모두 다 오버라이드 된 메소드로 작동한다