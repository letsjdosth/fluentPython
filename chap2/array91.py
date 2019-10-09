from array import array
from random import random

'''
first arg in array.array(arg,data)
Type code / C Type / Python Type / Minimum size in bytes
'b' / signed char / int / 1
'B' / unsigned char / int / 1
'u' / Py_UNICODE / Unicode character / 2
'h' / signed short / int / 2
'H' / unsigned short / int / 2
'i' / signed int / int/ 2
'I' / unsigned int / int / 2
'l' / signed long / int / 4
'L' / unsigned long / int / 4
'f' / float / float / 4
'd' / double / float / 8
'''

floats=array('d',(random() for i in range(10**2)))
print(floats[-1])

fp=open('floats.bin','wb') #bin: binary
floats.tofile(fp)
fp.close()

floats2=array('d')
fp=open('floats.bin','rb')
floats2.fromfile(fp,10**2)
fp.close()
print(floats2[-1])
print(floats2==floats)