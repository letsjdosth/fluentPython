#case1
b=6
def f1(a):
	print(a)
	print(b)

f1(3)
#3 #<-local
#6 #<-global
'''
>>> from dis import dis
>>> dis(f1)
  4           0 LOAD_GLOBAL              0 (print)
              2 LOAD_FAST                0 (a)
              4 CALL_FUNCTION            1
              6 POP_TOP

  5           8 LOAD_GLOBAL              0 (print)
             10 LOAD_GLOBAL              1 (b)     #<-자동으로 GLOBAL에서 불러온다
             12 CALL_FUNCTION            1
             14 POP_TOP
             16 LOAD_CONST               0 (None)
             18 RETURN_VALUE
'''



#case2
b=6
def f2(a):
	print(a)
	print(b)
	b=9

#f2(3)
#3 #<-local
#UnboundLocalError: local variable 'b' referenced before assignment #<-6이 안 나오고 에러남. 해당 print문 실행 시 global에 b가 있지만, 밑에 지역변수 b를 보고 그를 보아 에러가 난다

#이는 python 설계 결정사항. (대조적으로 javascript는 지역에서 var로 선언 없이 그냥 변수가 튀어나오는 이런 경우 바로 global에서 가져옴)
'''
>>> dis(f2)
 16           0 LOAD_GLOBAL              0 (print)
              2 LOAD_FAST                0 (a)
              4 CALL_FUNCTION            1
              6 POP_TOP

 17           8 LOAD_GLOBAL              0 (print)
             10 LOAD_FAST                1 (b)       #<-!!!!! 지역명 b를 로딩한다 (LOAD_GLOBAL이 아니라 LOAD_FAST)
             12 CALL_FUNCTION            1
             14 POP_TOP

 18          16 LOAD_CONST               1 (9)
             18 STORE_FAST               1 (b)
             20 LOAD_CONST               0 (None)
             22 RETURN_VALUE
'''


#case3
b=6
def f3(a):
	global b #<-함수 안에 할당 문장이 있으나, 그를 전역변수로 다루기 원할 시 global 명시
	print(a)
	print(b)
	b=9

f3(3)
#3 <-local
#6 <-global
print(b)
#9 <-global 변수를 가져가 다뤘으므로 9로 바뀌었다
b=30
print(b)
#30
'''
>>> dis(f3)
 32           0 LOAD_GLOBAL              0 (print)
              2 LOAD_FAST                0 (a)
              4 CALL_FUNCTION            1
              6 POP_TOP

 33           8 LOAD_GLOBAL              0 (print)
             10 LOAD_GLOBAL              1 (b)      #<-LOAD_GLOBAL을 사용한다
             12 CALL_FUNCTION            1
             14 POP_TOP

 34          16 LOAD_CONST               1 (9)
             18 STORE_GLOBAL             1 (b)      #<-마찬가지로 STORE_GLOBAL을 사용한다
             20 LOAD_CONST               0 (None)
             22 RETURN_VALUE
'''