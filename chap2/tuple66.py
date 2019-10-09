lax_coordinates=(33.9425, -118.408056)
city, year, pop, chg, area=('Tokyo', 2003, 32450, 0.66, 8014) #parallel assignment
traveler_ids=[('USA','31195855'),('BRA','CE342567'),('ESP','XDA205856')]

#tuple unpacking
for passport in sorted(traveler_ids):
	print('%s/%s'%passport)

for country, _ in traveler_ids: #_:dummy(case that we have no interest in)
	print(country)

latitude,longitude=lax_coordinates
print(latitude)
print(longitude)

#exchange variables
a,b=1,2
a,b=b,a
print(a,b)

#tuple unpacking when using function
print(divmod(20,8)) #(2,4)
t=(20,8)
quotient,remainder=divmod(*t) #함수 호출 시 *를 붙여 tuple unpacking 후 각 인자로 넘김
print(quotient,remainder)

#tuple unpacking of file path
import os
_,filename=os.path.split('/home/luciano/.ssh/idrsa.puh')
print(filename)


#using * when unpacking the tuple
a,b,*rest=range(5)
print(a,b,rest)

a,b,*rest=range(3)
print(a,b,rest)

a,b,*rest=range(2)
print(a,b,rest)

a, *body, c, d =range(5)
print(a,body,c,d)

*head,b,c,d=range(5)
print(head,b,c,d)


#nested tuple unpacking
metro_areas=[
	('Tokyo','JP',36.933,(35.689722,139.691667)),
	('Delhi NCR','IN',21.935,(28.613889,77.208889)),
	('Mexico City','MX',20.142,(19.433333,-99.133333)),
	('New York-Newark','US',20.104,(40.808611,-74.020386)),
	('Sao Paulo','BR',19.649,(-23.547778,-46.635833))
]
print('{:15}|{:^9}|{:^9}'.format('','lat.','long.'))
fmt='{:15}|{:9.4f}|{:9.4f}'
for name, cc, pop, (latitude,longitude) in metro_areas: #내부 형식과 맞으면 됨!
	if longitude<=0:
		print(fmt.format(name,latitude,longitude))