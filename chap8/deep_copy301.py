import copy

class Bus:
	def __init__(self, passengers=None):
		if passengers is None:
			self.passengers=[]
		else:
			self.passengers=list(passengers)
	def pick(self,name):
		self.passengers.append(name)
	def drop(self,name):
		self.passengers.remove(name)

bus1=Bus(['Alice','Bill','Claire','David'])
bus2=copy.copy(bus1)
bus3=copy.deepcopy(bus1)
print(id(bus1),id(bus2),id(bus3)) #2319766903384 2319766903608 2319766950072

bus1.drop('Bill')
print(bus2.passengers) #['Alice', 'Claire', 'David'] #copy.copy는 얕은 복사. 내포된 객체는 기존 객체의 참조만을 가져온다
print(id(bus1.passengers),id(bus2.passengers),id(bus3.passengers)) #2766515765832 2766515765832 2766517186120 #<-1,2의 것은 같은 객체다
print(bus3.passengers) #['Alice', 'Bill', 'Claire', 'David'] #copy.deepcopy는 깊은 복사. 내포된 객체를 새로 만든다


#깊은 복사 시 주의. 
#순환참조가 있거나 하면 무한루프
#너무 깊게 복사하는 경우도 있음(외부 리소스/싱글턴...)
#이런 문제 시, 객체에 __copy__(), __deepcopy__() 메소드를 구현하여 복사 동작 제어 가능

a=[10,20]
b=[a,30]
a.append(b)
print(a) #[10, 20, [[...], 30]]

c=copy.deepcopy(a)
print(c) #[10, 20, [[...], 30]] #<-copy.deepcopy()는 순환참조 처리를 위해 이미 복사한 객체의 참조를 기억 활요안다

