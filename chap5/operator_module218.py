from functools import reduce

def fact_lamb(n):
	'''factorial func not using recursive call'''
	return reduce((lambda a,b: a*b), range(1,n+1))

print(fact_lamb(5))

#사소한 익명함수 바로 가져다 쓸 수 있도록 간단한 연산자들을 operator module이 제공
#example
from operator import mul
def fact_mul(n):
	return reduce(mul,range(1,n+1))
print(fact_mul(5))


#operator.itemgetter() : 시퀀스에서 항목을 가져오는 함수를 반환 (직접 가져오는게 아니라, 가져오는 함수를!!!)
#itemgetter(1)==lambda fields:fields[1]
metro_data=[
	('Tokyo','JP',36.933,(35.689722,139.691667)),
	('Delhi NCR','IN',21.935,(28.613889,77.208889)),
	('Mexico City','MX',20.142,(19.433333,-99.133333)),
	('New York-Newark','US',20.104,(40.808611,-74.020386)),
	('Sao Paulo','BR',19.649,(-23.547778,-46.635833))
]
from operator import itemgetter
for city in sorted(metro_data,key=itemgetter(1)):
	print(city)

#itemgetter(2,5)==lambda fields: (fields[2],fields[5]) #function of returning tuple
cc_name=itemgetter(1,0)
for city in metro_data:
	print(cc_name(city))

#operator.attrgetter() : 이름으로 객체 속성을 추출하는 함수를 반환
#attrgetter('name')==lambda object:object.name
#attrgetter('name1','name2')==lambda object: (object.name(1),object.name(2))
from collections import namedtuple
LatLong=namedtuple('LatLong','lat long')
Metropolis=namedtuple('Metropolis','name cc poop coord')
metro_areas=[Metropolis(name,cc,pop,LatLong(lat,long)) for name,cc,pop,(lat,long) in metro_data]
print(metro_areas[0])
print(metro_areas[0].coord.lat)
from operator import attrgetter
name_lat=attrgetter('name','coord.lat')
for city in sorted(metro_areas,key=attrgetter('coord.lat')):
	print(name_lat(city))


#그외 operator module
import operator
print([name for name in dir(operator) if not name.startswith('_')])
#['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains', 'countOf', 'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt', 
# 'iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imatmul', 'imod', 'imul', 'index', 'indexOf', 'inv', 'invert', 'ior',
# 'ipow', 'irshift', 'is_', 'is_not', 'isub', 'itemgetter', 'itruediv', 'ixor', 'le', 'length_hint', 'lshift', 'lt', 'matmul',
# 'methodcaller', 'mod', 'mul', 'ne', 'neg', 'not_', 'or_', 'pos', 'pow', 'rshift', 'setitem', 'sub', 'truediv', 'truth', 'xor']
#i~는 복합할당(like +=) 연산자

#methodcaller() : 인수로 전달받은 객체의 메서드를 호출하는 함수를 반환
from operator import methodcaller
s='The time has come'
upcase=methodcaller('upper')
print(upcase(s)) #s.upper()
hiphenate=methodcaller('replace',' ','-')
print(hiphenate(s)) #s.replace(' ','-')

