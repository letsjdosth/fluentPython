#예: Sequence protocol
class Foo:
	def __getitem__(self, pos):
		return range(0,30,10)[pos]

#__getitem__은 Sequence의 속성
#Sequence는 (ABC 상속구조상) Container(__contains__), Iterable(__iter__)의 아래에 있고 이를 구현한다

f=Foo()
print(f[1])

for i in f: #<-정확히는 __iter__의 기능이지만, __getitem__이 있으므로 이를 가지고 프로토콜에 적절히 맞게 알아서 돌린다
	print(i)

print(20 in f) #<-정확히는 __contains__의 기능이지만, 마찬가지로 __getitem__이 있으므로 적절히 맞게 알아서 돌린다
print(15 in f)

#Foo가 모든 특별 메소드를 구현하지 않은 얼렁뚱땅 클래스이지만 어쨌든 시퀀스를 닮았으므로, 인터프리터는 동적으로 알아서 특별처리를 한다
