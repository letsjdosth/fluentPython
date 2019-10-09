#약한 참조:
#참조카운트(가비지콜렉팅시 0이면 메모리 청소)를 증가시키지 않고 객체를 참조함

import weakref

a_set={0,1}
wref=weakref.ref(a_set)
print(wref) #<weakref at 0x000001E8168F6688; to 'set' at 0x000001E816A0DAC8>

print(wref()) #{0, 1} #<-callable! #<-참조된 객체를 반환한다  #(콘솔에서는 wrep()만으로 호출하고, 그러면 암묵적으로 _ 변수에 결과값 {0,1}이 바인딩된다)

a_set={2,3,4}
print(wref) #<weakref at 0x000001E8168F6688; dead>
print(wref()) #None
print(wref() is None) #True

#참고: 위 코드는 콘솔에서는 다른 결과를 냄. 파이썬 콘솔은 None이 아닌 표현식의 결과에 _를 암묵적으로 할당하기 때문
#참고: 공식 문서에서는, weakref.ref으로 직접 .ref객체를 만들기보다는, weakref collection에 미리 정의된 자료형을 가져다쓰는 것을 권장하고 있음
#WeakKeyDictionary, WeakValueDictionary, WeakSet 등..


#WeakValueDictionary
class Cheese:
	def __init__(self,kind):
		self.kind=kind
	def __repr__(self):
		return 'Cheese(%r)'%self.kind

stock=weakref.WeakValueDictionary() #value가 이 dict에 의해 약한참조된다. 따라서 value로 쓰이는 객체의 (다른곳에서의) 참조 수가 0이 되면, 이 dict에서 제거된다.
catalog=[Cheese('Red Leicester'),Cheese('Tilsit'),Cheese('Brie'),Cheese('Parmesan')]
for cheese in catalog:
	stock[cheese.kind]=cheese

print(sorted(stock.keys())) #['Brie', 'Parmesan', 'Red Leicester', 'Tilsit']
del catalog
print(sorted(stock.keys())) #['Parmesan'] #<-!!!!!!!!!!!!!!!!!!!!!!! #다른 치즈 3종은 catalog가 사라지며 더이상 참조되지 않으므로 지워지고, 따라서 이 dict에서도 빠진다. Parmesan은 왜?
del cheese
print(sorted(stock.keys())) #[] #<-답: for문에 쓰인 cheese가 전역변수 취급이 되고 있고, cheese가 마지막으로 본 것이 Cheese('Parmesan')의 인스턴스 객체이기 때문

#WeakKeyDictionary: key를 약한참조로 데려온다. key로 쓰이는 객체가 더이상 참조되지 않으면, 이 dict에서 자동 제거된다.
#WeakSet : 마찬가지
#!!: 컨테이너 클래스를 만든다면, 혹은 스스로의 인스턴스를 다 알고 있도록 하는 클래스를 만든다면, list 대신 WeakSet을 쓰는것이 좋음(가비지 컬렉팅을 용이하게 하기 위하여)


#모든 객체가 약한 참조 대상이 될 수 있는 것은 아님
tstdic=dict()
try:
	weakref.ref(tstdic)
except TypeError:
	print("TypeError: cannot create weak reference to 'dict' object")
tstlst=list()
try:
	weakref.ref(tstlst)
except TypeError:
	print("TypeError: cannot create weak reference to 'list' object")
#list,dict는 안 됨. set은 됨. 그 외에 int, tuple은 안됨
#해결책 (list,dict의 경우)
class MyList(list):
	""""""

a_list=MyList(range(10))
try:
	weakref.ref(a_list)
	print("success!")
except TypeError:
	print("TypeError!")
#success!
#int,tuple 등은 야매로 상속한 클래스를 만들어도 안 됨 (이는 CPython의 구현상의 문제임)