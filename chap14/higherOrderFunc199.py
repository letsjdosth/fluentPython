fruits=['strawberry','fig','apple','cherry','raspberry','banana']
print(sorted(fruits,key=len)) #key로 함수를 받는다.(인수 1개인 함수는 모두 key로 줄 수 있다)

def reverse(word):
	return word[::-1]
print(reverse('testing'))
print(sorted(fruits,key=reverse))

'''
~functional programming~
each(func(x),array) : array의 각 값을 순회하며 func를 적용 (리턴 없음)
map(func(x), array) : array의 각 값을 func에 적용한 array를 리턴
filter(func(x),array) : array의 각 값 중 func에 적용 시 참인 값을 반환
reduce(func(x1,x2), array, initial) : array의 각 값을 순회하며, 처음엔 initial과 array[0]를 func에 넘김. 이후는, 이전순번에서 계산된 func값(즉,누적값)과 array[n]을 func에 넘김.
js:
function reduce(list, iter, memo) {
  var i = 0;
  if (Array.isArray(list)) {
    var res = (memo !== undefined ? memo : list[i++]); // <-- 남다른 결과값 선언부
    for (var len = list.length; i < len; i++) 
      res = iter(res, list[i], i, list);
    }
  return res
}
anonymous func ==lambda func
'''

#python3에서: map,filter는 존재하나, listcomp/generator를 이용하여 같은 작업을 모두 할 수 있고, 가독성에서는 listcomp가 더 나음
#python3에서 map,filter는 generator(iterable) 반환. python2에서는 list 반환
def factorial(n):
	'''returns n!'''
	return 1 if n<2 else n*factorial(n-1)
fact=factorial
print(list(map(fact,range(6)))) #map
print([fact(n) for n in range(6)]) #listcomp

print(list(map(factorial,filter(lambda n:n%2, range(6))))) #filter+map
print([factorial(n) for n in range(6) if n%2]) #listcomp


#reduce()
from functools import reduce #python3부터는 reduce는 내장이 아님
def add(a,b):
	return a+b
print(reduce(add,range(100))) #reduce
print(sum(range(100))) #just func


#lambda function
#!!: python lambda에서는 람다함수 본체가 순수한 표현식으로만 구성되도록 제한됨. 할당문, 루프, try 등 불가
#형식: lambda 매개변수 : 반환값
print(sorted(fruits,key=lambda word: word[::-1])) #위의 reverse를 lambda로 바로 구현
print(list(map(lambda x: x + 10, [1, 2, 3])))

