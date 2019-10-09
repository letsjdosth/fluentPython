def factorial(n):
	'''returns n!'''
	return 1 if n<2 else n*factorial(n-1)

print(factorial(42))
print(factorial.__doc__)
print(type(factorial)) #<class 'function'>


fact=factorial
print(fact)
fact(5)
print(map(factorial,range(11)))
print(list(map(factorial,range(11))))

#map(function_to_apply, list_of_inputs)
#iterable한 list_of_inputs의 각 항목을 function_to_apply에 적용. 그 값을 다시 iterable한 객체(map object)로 반환