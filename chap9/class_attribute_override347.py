from vector2d_v3_334 import Vector2d #<-slots를 적용한 버전을 가져다 쓰면, read-only attribute라는 에러메시지가 뜸
v1=Vector2d(1.1, 2.2)
dumpd=bytes(v1)
print(dumpd, len(dumpd)) #b'd\x9a\x99\x99\x99\x99\x99\xf1?\x9a\x99\x99\x99\x99\x99\x01@' 17 #<-1+8+8


#인스턴스 속성 변경
v1.typecode='f' #v1 인스턴스에서 array에 들어가는 자료형 코드를 바꾼다. 기존 double 8byte 에서 float 4byte로 바꾸었다
dumpf=bytes(v1)
print(dumpf, len(dumpf)) #b'f\xcd\xcc\x8c?\xcd\xcc\x0c@' 9 #<-float로 bytes화되었다. 1+4+4로 9byte가 되었다

print(Vector2d.typecode) #클래스 기본정의는 여전히 'd'이다. v1 객체만 'f로 변경되었다'



#클래스 속성을 변경하려면 클래스 정의를 직접 바꿔야 하며, 인스턴스를 변경하면 해당 인스턴스로만 한정될 뿐임
Vector2d.typecode='f' #<-클래스 자체를 바꾼다 typecode overriding
v2=Vector2d(1.1, 2.2)
dump2f=bytes(v2)
print(dump2f, len(dump2f)) #b'f\xcd\xcc\x8c?\xcd\xcc\x0c@' 9 #<-다른 옵션 없이도 바로 f로 적용되었다



#하지만 overriding보다 좋은 방법은, 상속해서 커스터마이즈 하는 것임. 기존 객체의 쓰임과 충돌하지 않고,또한 코드의 의도가 명백히 보이기 때문
Vector2d.typecode='d' #<-돌려놓고
class ShortVector2d(Vector2d):
	typecode='f' #<-커스터마이즈할 요소만 덮어쓴 자식 클래스를 만들자

sv=ShortVector2d(1/11, 1/27)
dumpsv=bytes(sv)
print(dumpsv,len(dumpsv)) #b'f\x8c.\xba=&\xb4\x17=' 9