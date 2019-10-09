import itertools
#주의! 아래 예의 대부분은 itertools에 있지만, 기본 내장형도 섞여있으니 잘 볼 것
#주의! 파이썬 전체 라이브러리를 보면, os나 functools 등에도 있음. 여기에서는 기본 / itertools에 있는 요소를 중심으로 보여줌


#필터링 제너레이터 함수
#참고: 인수 predicate는, 자체로 인수 하나를 받아 불리언을 반환하는 함수
def vowel(c):
	'''예시를 위한 predicate용 함수 정의'''
	return c.lower() in 'aeiou'

f=filter(vowel,'Aardvark') #filter(predicate, it)
print(f,next(f),list(f)) #<filter object at 0x00000141E126D1D0> A ['a', 'a']

f=itertools.filterfalse(vowel,'Aardvark') #filterfalse(predicate, it)
print(f,next(f),list(f)) #<itertools.filterfalse object at 0x0000020FA347DEF0> r ['d', 'v', 'r', 'k']

f=itertools.dropwhile(vowel,'Aardvark') #dropwhile(predicate,it) #predicate가 참인 값인 동안 항목들을 지나가면서 it을 소비. 이후 거짓이 되면 추가검사 없이 남은 항목 모두 생성
print(f,next(f),list(f)) #<itertools.dropwhile object at 0x000001A3548D1BC8> r ['d', 'v', 'a', 'r', 'k']

f=itertools.takewhile(vowel,'Aardvark') #takewhile(predicate,it) #predicate가 참인 동안 항목을 생성. 이후 추가검사 없이 멈춤
print(f,next(f),list(f)) #<itertools.takewhile object at 0x0000026AFFEE1CC8> A ['a']

f=itertools.compress('Aardvark',(1,0,1,1,0,1)) #compress(it, selector_it) #2개의 반복형을 병렬로 소비. selector_it이 참일때마다 그에 대응하는 it을 생성
print(f,next(f),list(f)) #<itertools.compress object at 0x0000029565ACD0B8> A ['r', 'd', 'a']

f=itertools.islice('Aardvark',4) #islice(it,stop) 혹은 islice(it, start, stop, step=1) #느긋한 슬라이싱
print(f,next(f),list(f)) #<itertools.islice object at 0x0000016BD0A06688> A ['a', 'r', 'd']

f=itertools.islice('Aardvark',4,7) 
print(f,next(f),list(f)) #<itertools.islice object at 0x000002AD078FA688> v ['a', 'r']

f=itertools.islice('Aardvark',4,7,2)
print(f,next(f),list(f)) #<itertools.islice object at 0x000002AD078D6688> v ['r']


#매핑 제너레이터 함수
sample=[5,4,2,8,7,6,3,0,9,1]

m=itertools.accumulate(sample) #accumulate(it,[func]) #누적된 합계. func를 제공하면 처음 두 개의 항목에 func를 적용한 결과를 첫 값으로 생성하여 it을 반복 (reduce와 비슷하나 중도의 제너레이터를 준다)
print(m,next(m),list(m)) #<itertools.accumulate object at 0x0000029877E3A0C8> 5 [9, 11, 19, 26, 32, 35, 35, 44, 45]

m=itertools.accumulate(sample, min)
print(m,next(m),list(m)) #<itertools.accumulate object at 0x0000022C8761A1C8> 5 [4, 2, 2, 2, 2, 2, 0, 0, 0]

m=itertools.accumulate(sample,max)
print(m,next(m),list(m)) #<itertools.accumulate object at 0x00000220EED2C288> 5 [5, 5, 8, 8, 8, 8, 8, 9, 9]

import operator
m=itertools.accumulate(sample,operator.mul)
print(m,next(m),list(m)) #<itertools.accumulate object at 0x000001745D9DA708> 5 [20, 40, 320, 2240, 13440, 40320, 0, 0, 0]

m=itertools.accumulate(range(1,11),operator.mul)
print(m,next(m),list(m)) #<itertools.accumulate object at 0x000001AD6A9AA7C8> 1 [2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800] #<-팩토리얼!

m=enumerate('albatroz',1) #enumerate(it,start=0) #숫번을 매긴 튜플을 생성한다
print(m,next(m),list(m)) #<enumerate object at 0x0000013E0AACA630> (1, 'a') [(2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'r'), (7, 'o'), (8, 'z')]

m=map(operator.mul, range(11), range(11)) #map(func, it1[, it2,...]) #it을 차례대로 func에 넣어 나온 값을 생성한다. func의 인수가 여러개면 여러개의 it을 넘겨야 하며, 병렬로 소비한다
print(m,next(m),list(m)) #<map object at 0x000002A06246DF28> 0 [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

m=itertools.starmap(operator.mul, enumerate('albatroz',1)) #starmap(func,it) #it의 각 항목을 *iit로 받아 func(*iit)를 적용한 값을 생성한다
print(m,next(m),list(m)) #<itertools.starmap object at 0x0000021B2670D8D0> a ['ll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']

m=itertools.starmap(lambda a,b: b/a, enumerate(itertools.accumulate(sample), 1)) #급한 버전: starmap(lambda a,b:b/a, zip([1,2,3,4,5,6,7,8,9,10],[5, 9, 11, 19, 26, 32, 35, 35, 44, 45]) 
print(m,next(m),list(m)) #<itertools.starmap object at 0x0000020DD7E4E278> 5.0 [4.5, 3.6666666666666665, 4.75, 5.2, 5.333333333333333, 5.0, 4.375, 4.888888888888889, 4.5]


#병합 제너레이터 함수
#순차소비
a=itertools.chain('ABC',range(2))
print(a,next(a),list(a)) #<itertools.chain object at 0x000001E182E1D940> A ['B', 'C', 0, 1]

a=itertools.chain.from_iterable(enumerate('ABC')) #from_iterable(it) #it을 봤을 때 반복형 안의 반복형객체가 있는 경우. 받아서 모조리 편다
print(a,next(a),list(a)) # #<itertools.chain object at 0x000001C7AED55320> 0 ['A', 1, 'B', 2, 'C']

#병렬소비
a=zip('ABC',range(5)) #병렬로 하나씩 꺼내 튜플을 생성하는 제너레이터 #짧은데에 맞춰 끊는다
print(a,next(a),list(a)) #<zip object at 0x00000258AA675D88> ('A', 0) [('B', 1), ('C', 2)]  

a=zip('ABC',range(5),[10,20,30,40]) #<-둘 이상의 인수도 받을 수 있다
print(a,next(a),list(a)) #<zip object at 0x0000028BA0205F48> ('A', 0, 10) [('B', 1, 20), ('C', 2, 30)] #<-여러개도 된다


a=itertools.zip_longest('ABC',range(5)) #긴쪽에 맞추어 늘린다
print(a,next(a),list(a)) #<itertools.zip_longest object at 0x0000028BA02094F8> ('A', 0) [('B', 1), ('C', 2), (None, 3), (None, 4)] #모자르면 기본적으로 None을 채운다

a=itertools.zip_longest('ABC',range(5),[10,20,30,40],fillvalue='?') #fillvalue를 넘겨 None 대신 다른 값으로 채울 수 있다
print(a,next(a),list(a)) #<itertools.zip_longest object at 0x0000018463419548> ('A', 0, 10) [('B', 1, 20), ('C', 2, 30), ('?', 3, 40), ('?', 4, '?')]

#데카르트곱
a=itertools.product('abc',range(2)) #병합가능한 모든 경우의 수를 튜플로 묶는다 (겹 for문과 비슷하게 동작)
print(a,next(a),list(a)) #<itertools.product object at 0x0000022021B8C630> ('a', 0) [('a', 1), ('b', 0), ('b', 1), ('c', 0), ('c', 1)]

suits='spades hearts diamonds clubs'.split()
a=itertools.product('AK',suits)
print(a,next(a),list(a)) #<itertools.product object at 0x000002C0CA3CC798> ('A', 'spades') [('A', 'hearts'), ('A', 'diamonds'), ('A', 'clubs'), ('K', 'spades'), ('K', 'hearts'), ('K', 'diamonds'), ('K', 'clubs')]

a=itertools.product('ABC') #<-하나만 넘길수도 있으나... 그리 유용하지 않다...
print(a,next(a),list(a)) #<itertools.product object at 0x000001E64121C630> ('A',) [('B',), ('C',)] 

a=itertools.product('ABC',repeat=2) #repeat를 넘겨 각 반복형을 여러 번 소비할 수 있다. product('ABC','ABC')와 같다
print(a,next(a),list(a)) #<itertools.product object at 0x000001E4054BC630> ('A', 'A') [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]

a=itertools.product('AB',range(2),repeat=2) #product('AB',range(2),'AB',range(2))와 같다
print(a,next(a),list(a)) #<itertools.product object at 0x000001DE1786C630> ('A', 0, 'A', 0) [('A', 0, 'A', 1), ('A', 0, 'B', 0), ('A', 0, 'B', 1), ('A', 1, 'A', 0), ('A', 1, 'A', 1), ('A', 1, 'B', 0), ('A', 1, 'B', 1), ('B', 0, 'A', 0), ('B', 0, 'A', 1), ('B', 0, 'B', 0), ('B', 0, 'B', 1), ('B', 1, 'A', 0), ('B', 1, 'A', 1), ('B', 1, 'B', 0), ('B', 1, 'B', 1)]


#확장 제너레이터 함수
e=itertools.count() #count(start=0,step=1)
print(next(e),next(e)) # 0 1 #<-무한히 간다

se=itertools.islice(itertools.count(1,0.3),5)
print(se,next(se),list(se)) #<itertools.islice object at 0x000001751F68A3B8> 1 [1.3, 1.6, 1.9000000000000001, 2.2]

e=itertools.cycle('ABC')
print(next(e),next(e),next(e),next(e)) #A B C A

se=itertools.islice(itertools.cycle('ABC'),7)
print(se,next(se),list(se)) #<itertools.islice object at 0x0000022FEA25A3B8> A ['B', 'C', 'A', 'B', 'C', 'A']

e=itertools.repeat(7) #repeat(item[,times])
print(next(e),next(e),next(e)) #7 7 7 #<-무한히 간다

e=itertools.repeat(8,4)
print(list(e)) #[8, 8, 8, 8]

me=map(operator.mul, range(11), itertools.repeat(5)) #<-map이 앞 인수의 길이에 맞춰 11번 next를 호출하므로, 5를 11번 반복해 생성하게 된다
print(list(me)) #[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]


#순열조합(combinatoric) 제너레이터 함수
#(공식문서 상) product도 이에 속한다
cp=itertools.combinations('ABC',2) #조합
print(cp,next(cp),list(cp)) #<itertools.combinations object at 0x000001681E06A458> ('A', 'B') [('A', 'C'), ('B', 'C')]

cp=itertools.combinations_with_replacement('ABC',2) #반복추출 가능 조합
print(cp,next(cp),list(cp)) #<itertools.combinations_with_replacement object at 0x000002494EDEA3B8> ('A', 'A') [('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]

cp=itertools.permutations('ABC',2) #순열
print(cp,next(cp),list(cp)) #<itertools.permutations object at 0x00000172AA5BA888> ('A', 'B') [('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

cp=itertools.product('ABC',repeat=2) #데카르트곱 #(위에도 있지만 다시 비교)
print(cp,next(cp),list(cp)) #<itertools.product object at 0x00000276FD46C798> ('A', 'A') [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]


#재배치 제너레이터 함수
r=itertools.groupby('LLLLAAGGG') #groupby(it, key=None) #(key,group)의 튜플 생성. 인수(콜러블) 및 반환값(콜러블의 반환값) key는 그룹화 기준, group은 it에서 그에 해당하는 순회가능한 반복자이다
print(r,next(r),list(r)) #<itertools.groupby object at 0x000002961CAAB3B8> ('L', <itertools._grouper object at 0x000002961CAA2A20>) [('A', <itertools._grouper object at 0x000002961CAA29E8>), ('G', <itertools._grouper object at 0x000002961CAA2A90>)]
for char,group in itertools.groupby('LLLLAAGGG'):
	print(char,'->',list(group))
# L -> ['L', 'L', 'L', 'L']
# A -> ['A', 'A']
# G -> ['G', 'G', 'G']

animals=['duck','eagle','rat','giraffe','bear','bat','dolphin','shark','lion']
animals.sort(key=len) #주의. groupby를 사용하려면 it이 해당 key에 따라 군집화되어있어야 한다. 가장 쉬운 방법은 정/역방향 정렬
r=itertools.groupby(animals,len)
for length,group in r:
	print(length,'->',list(group))
# 3 -> ['rat', 'bat']
# 4 -> ['duck', 'bear', 'lion']
# 5 -> ['eagle', 'shark']
# 7 -> ['giraffe', 'dolphin']

r=reversed('abcdefg')
print(r,next(r),list(r)) #<reversed object at 0x000001AC26E21D68> g ['f', 'e', 'd', 'c', 'b', 'a']

for length,group in itertools.groupby(reversed(animals),len):
	print(length,'->',list(group))
# 7 -> ['dolphin', 'giraffe']
# 5 -> ['shark', 'eagle']
# 4 -> ['lion', 'bear', 'duck']
# 3 -> ['bat', 'rat']


#tee 제너레이터 함수
#tee(it): it의 요소를 하나씩 생성하는, 독립된 반복자를 2개 생성해 반복자의 튜플로 반환한다.
t=itertools.tee('ABC')
print(t) #(<itertools._tee object at 0x00000176C23606C8>, <itertools._tee object at 0x00000176C2360408>) #<-일단 2개다
g1,g2=itertools.tee('ABC')
print(next(g1),next(g2),next(g2),list(g1),list(g2)) # A A B ['B', 'C'] ['C'] #<-독립된 반복자이다

print(list(zip(*itertools.tee('ABC')))) #[('A', 'A'), ('B', 'B'), ('C', 'C')]
