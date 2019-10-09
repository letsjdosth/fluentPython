#책에서의 method_is_descriptor.py

import collections


class Text(collections.UserString):
	def __repr__(self):
		return 'Text({!r})'.format(self.data)

	def reverse(self):
		return self[::-1]

word=Text('forward')
print(repr(word)) #Text('forward')
print(repr(word.reverse())) #Text('drawrof')

#(인스턴스가 아닌) 클래스에서 바로 메소드 호출
print(type(Text.reverse), type(word.reverse)) #<class 'function'> <class 'method'>
print(repr(Text.reverse(Text('forward')))) #Text('drawrof') #<-클래스로 호출한 메소드는 그냥 함수로 작동한다.
print(list(map(Text.reverse, ['repaid',(10,20,30),Text('stressed')]))) #['diaper', (30, 20, 10), Text('desserts')] #<-마찬가지로 클래스로 호출하면 자기객체가 아니어도 (문제가 없다면) 일반 함수처럼 작동한다.

#__get__을 직접 호출해보기
print(Text.reverse.__get__(word)) #<bound method Text.reverse of Text('forward')> #<-객체를 전달해 __get__을 호출하면 해당 객체에 바인딩된 메서드가 반환된다.
print(Text.reverse.__get__(None,Text)) #<function Text.reverse at 0x03C493D8> #<-instance로 None을 전달하면 함수 자신이 반환된다.

print(repr(word.reverse)) #<bound method Text.reverse of Text('forward')> #<-실제로 23번째줄과 같이 동작한다.
print(repr(word.reverse.__self__)) #Text('forward') #<-바인딩된 객체는 __self__에 호출된 객체에 대한 참조를 담고 있다.
print(word.reverse.__func__ is Text.reverse) #True #<-(!!)바인딩된 메서드는 원래 함수를 참조한다.