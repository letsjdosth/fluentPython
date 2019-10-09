import numpy

a=numpy.arange(12)
print(type(a),a.shape,a) #<class 'numpy.ndarray'> 
a.shape=(3,4)
print(a)
print(a[2])
print(a[2,1])
print(a[:,1])
print(a.transpose())

