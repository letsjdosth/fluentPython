#yield from

#사용처 1: for 루프 안 yield의 단축 (chap14 yield_from_basic535.py와 동일)
#예1
def gen():
	for c in 'AB':
		yield c
	for i in range(1,3):
		yield i

def gen2(): #gen()과 완전히 동일하다
	yield from 'AB'
	yield from range(1,3)

print(list(gen())) #['A', 'B', 1, 2]
print(list(gen2())) #['A', 'B', 1, 2]


#예2
def chain(*iterables):
	"""iterables를 모두 이어서 차례대로 반환하는 제너레이터"""
	for it in iterables:
		yield from it

s='ABC'
t=tuple(range(3))
print(list(chain(s,t))) #['A', 'B', 'C', 0, 1, 2]

# Example of flattening a nested sequence using subgenerators



#예3: Python Cookbook 3E 예제
from collections import Iterable

def flatten(items, ignore_types=(str, bytes)):
	""" Example of flattening a nested sequence using subgenerators"""
	for x in items:
		if isinstance(x, Iterable) and not isinstance(x, ignore_types):
			yield from flatten(x) #<-item의 내부 요소가 iterable이면 그걸 까서 각 요소를 자기자신에 다시 넘겨버린다
		else:
			yield x #<-iterable이 아니면 바로 생성한다


items = [1, 2, [3, 4, [5, 6], 7], 8]
for x in flatten(items):
	print(x)
print(list(flatten(items))) #[1, 2, 3, 4, 5, 6, 7, 8]

items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
	print(x)
print(list(flatten(items))) #['Dave', 'Paula', 'Thomas', 'Lewis']