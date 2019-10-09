#aliasing: 한 객체에 여러 레이블을 붙이는 것

charles={'name':'Charles L. Dodgson','born':1832}
lewis=charles #<-별명 설정!
assert lewis is charles
print(id(charles),id(lewis)) #1961924127408 1961924127408

lewis['balance']=950
print(charles) #{'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}


alex={'name':'Charles L. Dodgson','born':1832,'balance':950} #<-같은 내용을 alex에 따로 할당한다
print(alex==charles) #True. ==로 평가한 내용(값)은 같다
print(alex is charles) #False #<-!!!!!! 같은 객체는 아님. is 연산자는 id()를 비교하며, id는 객체마다 고유하게 붙는다(CPython에서는 메모리 주소에 대응하는 정수값)
assert alex is not charles

#객체는 : 정체성(메모리 주소 혹은 ID), 자료형(TYPE), 값(VALUE) 을 각각 가지고 있음

