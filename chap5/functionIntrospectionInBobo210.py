import bobo

@bobo.query('/')
def hello(person):
	return 'Hello %s!'%person

#in cmd, bobo -f functionIntrospectionInBobo210.py

#in localhost:8080,
#Missing form variable person 


#in http://localhost:8080/?person=Jim
#Hello Jim!