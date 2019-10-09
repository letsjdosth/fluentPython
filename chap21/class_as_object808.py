#준비
class TestSuperClass:
	pass

class TestClass(TestSuperClass):
	a=1
	def b_method(self):
		pass

class TestSubClass(TestClass):
	pass

#일반적인 
print(dir(TestClass))
print(TestClass.__dict__)

#dir에 안보이는것도 있다..
#공식 문서:
#dir() 은 주로 대화형 프롬프트에서의 사용 편의를 위해 제공되기 때문에, 엄격하거나 일관되게 정의된 이름 집합을 제공하기보다 흥미로운 이름 집합을 제공하려고 시도하며, 상세한 동작은 배포마다 변경될 수 있습니다. 
#예로, 인자가 클래스면 메타 클래스 어트리뷰트는 결과 리스트에 없습니다. 

#안보이는.. 메타클래스 어트리뷰트
print(TestClass.__bases__) #(<class '__main__.TestSuperClass'>,) #슈퍼클래스를 담은 튜플
print(TestClass.__qualname__) #TestClass #전역 범위부터 클래스를 담은 모듈까지의 경로를 점으로 구분한, 클래스나 함수의 경로명.
print(TestClass.__subclasses__()) #[<class '__main__.TestSubClass'>] #현재 메모리에 존재하는 해당 클래스 바로 아래 서브클래스의 리스트 반환
#TestClass.mro() #<-__mro__로 클래스 생성 시 호출. 메타클래스는 이 메서드를 오버라이드해서 현재 생성중인 클래스의 mro를 커스터마이즈할 수 있음.