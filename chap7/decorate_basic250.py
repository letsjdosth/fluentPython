'''
@decorate
def target():
	print('running target()')

==

def target():
	print('running target()')

target=decorate(target)
'''



def deco(func):
	def inner():
		print('running inner()')
	return inner

@deco
def target():
	print('running target(')

target() #'running inner()' #<-대체되었다
print(target) #<function deco.<locals>.inner at 0x000002125BED0158>  #<- inner()를 가르키고 있다

