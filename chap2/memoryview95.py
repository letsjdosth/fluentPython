import array
numbers=array.array('h',[-2,-1,0,1,2]) #'h' / signed short / int / 2

memv=memoryview(numbers)
print(len(memv))
print(memv[0])
memv_oct=memv.cast('B') #'B' / unsigned char / int / 1 #cast()는 해당 type으로 보는 memoryview 객체를 반환한다.
print(memv_oct.tolist()) #len이 8임. unsigned short(2byte)가 char형(1byte)으로 바뀌어서 그럼
memv_oct[5]=4
print(numbers) #memv_oct와 memv는 같은 애(number)를 계속 보고있음.(line4). unsigned int 4의 상위바이트는 1024