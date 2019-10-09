symbols='$¢£¥€¤'
print(tuple(ord(symbol) for symbol in symbols))

import array

print(array.array('I',(ord(symbol) for symbol in symbols))) #I: unsigned int
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

colors=['black','white']
sizes=['S','M','L']
for tshirt in ('%s %s' % (c,s) for c in colors for s in sizes):
	print(tshirt)