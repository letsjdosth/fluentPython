from collections import namedtuple
City=namedtuple('City','name country population coordinates') #namedtuple(class_name, field_name(공백으로 구분))
tokyo=City('Tokyo','JP',36.933,(35.689722,139.691667))
print(tokyo)
print(tokyo.population)
print(tokyo.coordinates)
print(tokyo[1])

#attributes of namedtuple
print(City._fields)

LatLong=namedtuple('LatLong','lat long') #namedtuple(class_name, field_name(공백으로 구분))
delhi_data=('Delhi NCR','IN',21.935,LatLong(28.613889,77.208889))
delhi=City._make(delhi_data) #== City(*delhi_data)
print(delhi._asdict()) #return OrderedDict

for key,value in delhi._asdict().items():
	print(key+":",value)
