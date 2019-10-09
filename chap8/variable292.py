#label
a=[1,2,3]
b=a
a.append(4)
print(b) #[1, 2, 3, 4]



#order of assignment
class Gizmo:
	def __init__(self):
		print('Gizmo id: %d' % id(self))

x=Gizmo() #Gizmo id: 2692673296592

try:
	y=Gizmo()*10
#Gizmo id: 2692673296144
#    y=Gizmo()*10
#TypeError: unsupported operand type(s) for *: 'Gizmo' and 'int'
#위에서, 객체는 생성되었으나, 10을 못 곱해서 에러남

except TypeError:
	pass

print(dir())
#['Gizmo', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a', 'b', 'x']
#y가 없음. 할당문은 오른쪽부터 실행됨
#변수를 잡아둔 후 그 박스에 오른쪽 할당 내용을 만들어 넣는 것이 아님
#오른쪽에서 먼저 만들고 거기에 = 왼쪽의 꼬리표를 다는 것
