#context manager
#콘텍스트 관리자 프로토콜: (with를 사용할) 객체에 __enter__(), __exit__() 구현

with open('context_manager_mirror556.py',encoding='utf8') as fp:
	src=fp.read(60)
#with 진입 시, '콘텍스트 관리자'는 with 뒤의 표현식을 평가한 객체가 됨. 이후 그 객체의 __enter__() 호출 결과를 as 뒤 변수에 바인딩 
#(<-따라서 with 뒤에 들어오는 '객체에' 콘텍스트 관리자 프로토콜을 구현해야 함. !!!with 연산자를 구현하는것이 아님.)
#위 with문에서는, open()이 TextIOWrapper를 반환하고, 이후 그 TextIOWrapper의 __enter__()는 self를 반환함. 따라서 fp는 해당 객체의 참조(별명)가 됨

#with 블록을 빠져나갈 시, '콘텍스트 관리자'의 __exit__()이 호출됨. 즉, open()이 반환한 TextIOWrapper의 __exit__이 동작
#주의할 점은, as 뒤 변수의 __exit__이 아니라는 것임.

#참고: with문의 as는 선택적임. __enter__()의 리턴이 없으면 굳이 없어도 됨



print(len(src)) #(!! with 블록은 스코프를 정의하지 않는다)
print(fp) #<_io.TextIOWrapper name='mirror.py' mode='r' encoding='utf8'> #<-with 블록 밖에서도 as에 쓴 변수까지 살아있다 (!! with 블록은 스코프를 정의하지 않는다)
print(fp.closed, fp.encoding) #True utf8 #<-속성을 여전히 읽을 수 있다. 파일이 닫혔다.
try:
	fp.read(60)
except ValueError as e:
	print('VaoueError:',e) #VaoueError: I/O operation on closed file. #<-읽을 수 없다