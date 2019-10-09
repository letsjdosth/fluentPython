a=dict(one=1,two=2,three=3)
b={'one':1,'two':2,'three':3}
c=dict(zip(['one','two','three'],[1,2,3]))
d=dict([('two',2),('one',1),('three',3)])
e=dict({'three':3,'one':1,'two':2})
print(a==b==c==d==e)


dial_codes=[
	(86,'China'),
	(91,'India'),
	(1,'United States'),
	(62,'Indonesia'),
	(55,'Brazil'),
	(92,'Pakistan'),
	(880,'Bangladesh'),
	(234,'Nigeria'),
	(7,'Russia'),
	(81,'Japan')
]
country_code={country:code for code, country in dial_codes}
print(country_code)
result={code:country.upper() for country, code in country_code.items() if code<66}
print(result)


