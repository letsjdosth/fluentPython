#파이썬에는, 자바처럼 언어가 지원하는 비공개/보호(private/protected)속성이 없음
#단, 관례적인 방법들이 있음

#1. __(name mangling (이름 장식) / 유사-private)
#객체 내 어트리뷰트 이름을 __로 시작하면,(끝은 __가 아닐 경우)
#인터프리터는 __dict__에 key(즉 속성명)를 _class명__어트리뷰트명 으로 변환하여 저장함

from vector2d_v3_334 import Vector2d
v1=Vector2d(3,4)
print(v1.__dict__) #{'_Vector2d__x': 3.0, '_Vector2d__y': 4.0} #<-'_클래스이름'이 붙었다

#상속시 이름 충돌을 피하기 위해 이를 사용할 수 있음 
#(하지만 상속 문제를 고려한다면 명시적으로 어트리뷰트의 이름을 구분되도록 충분히 장식하는 것이 나음)

#__는 보안기능/ 혹은 완벽한 private 기능은 아님. 실수로 접근하는것을 막도록 설계된 것이지, 고의로 접근하는것을 막지는 못함
try:
	v1.x=6
except AttributeError as e:
	print(e)
#can't set attribute. except문에 걸린다
#위의 경우는 막혔다. 일반적으로 자연스러운 방식으로 접근 시 에러를 뱉는다.

try:
	v1._Vector2d__x=8.0
	print(v1)
except AttributeError as e:
	print(e)
#에러없이 실행되고 (8.0, 4.0)가 출력된다.
#직접 속성을 완전히 입력해 접근하면 접근할 수 있다. #(이는 직렬화/디버깅을 위함임)



#2. _ (관례적 protected 혹은 관례적 private (자바의 protected와는 다름!))
#객체 내 어트리뷰트 이름을 _로 시작하면
#인터프리터는 아무것도 하지 않음. 
#하지만 파이썬 코더들의 관례로 _로 시작하는 어트리뷰트를 클래스 외부에서 접근하지 않는 것으로 자리잡혀 있음
#(마치 상수를 대문자 변수명으로 쓰듯)

class ProtectedDemo:
	_x=6

v2=ProtectedDemo()
v2._x=7
print(v2._x) #7 <-접근/변경이 다 먹음. 하지만 _x에 대한 직접 접근은 커뮤니티 관례적으로 하지 말자는 것임