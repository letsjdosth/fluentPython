#제너레이터 표현식
#listcomp와 비슷하지만, 시작시 리스트를 한꺼번에 안 만들고, 대신 next()가 호출될 때 요소를 하나씩 만들어서 돌려준다

def gen_AB():
	print('start')
	yield 'A'
	print('continue')
	yield 'B'
	print('end.')

res1=[x*3 for x in gen_AB()] #listcomp
#start
#continue
#end.
#in 뒤에 제너레이터를 받았지만, listcomp는 한번에 전체 리스트를 만드므로, 느긋한 구현을 제대로 써먹지 못한다

for i in res1:
	print('-->',i)
# --> AAA
# --> BBB


res2=(x*3 for x in gen_AB()) #gen-exp. 제너레이터 표현식 (튜플 컴프리헨션이 아니다). #출력이 없다. gen_AB가 아직 한 줄도 실행되지 않았다
print(res2) #<generator object <genexpr> at 0x00000155C70CA888> #<-제너레이터다
for i in res2:
	print('-->',i)
#start   #<-gen_AB의 첫줄이 이제 실행된다
#--> AAA
#continue
#--> BBB
#end.


