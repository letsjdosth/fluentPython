#대부분의 내장 클래스/사용자정의 클래스 자체의 타입은 type. type은 메타클래스
print('spam'.__class__) #<class 'str'>
print(str.__class__) #<class 'type'>

from bulkfood_v6 import LineItem
print(LineItem.__class__) #<class 'type'>
print(type.__class__) #<class 'type'> #<-type의 타입은 자기 자신의 객체로 정의됨

import collections.abc
import abc
print(collections.abc.Iterable.__class__) #<class 'abc.ABCMeta'> #<-표준 라이브러리에는 type이 아닌 다른 종류의 메타클래스도 있다.
print(abc.ABCMeta.__class__) #<class 'type'> #<-다시 type이다. 메타클래스는 type의 서브클래스.
print(abc.ABCMeta.__mro__) #(<class 'abc.ABCMeta'>, <class 'type'>, <class 'object'>)
#모든 객체는 object를 상속받음. 
#'클래스'(정의)자체도 객체로 만들어져 있고, 이는 type의 객체.
#object도 type객체.(object의 type은 type). type은 object의 서브클래스.