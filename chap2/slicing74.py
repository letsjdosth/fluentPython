#slicing
l=[10,20,30,40,50,60]
print(l[:2])
print(l[2:]) #자를 때 같은 인덱스로 자르면 됨 (중단점이 해당 항목을 포함하지 않으므로)
print(l[:3])
print(l[3:])

s='bicycle'
print(s[::3]) #seq[start:stop:step]=seq.__getitem__(slice(start,stop,step))
print(s[::-1])
print(s[::-2])


#slice instance
invoice_data=[(1909,'Pimoroni Pibrella',17.50,3,52.50),
	(1489,'6mm Tactile Switch x20',4.95,2,9.90),
	(1510,'Panavise Jr. - Pv-201',28.00,1,28.00),
	(1601,'PiTFT Mini Kit 320x240',34.95,1,34.95)
]
invoice='\n'+'0'+'.'*5+'6'+'.'*33+'40'+'.'*10+'52'+'.'*1+'55'+'.'*8+'\n'
for data in invoice_data:
	a,b,c,d,e=data
	invoice+='{:<6}{:34}{:<12}{:<3}{:<8}\n'.format(a,b,c,d,e)

print(invoice)

SKU=slice(0,6)
DESCRIPTION=slice(6,40)
UNIT_PRICE=slice(40,52)
QUANTITY=slice(52,55)
ITEM_TOTAL=slice(55,None)

line_items=invoice.split('\n')[2:]
for item in line_items:
	print(item[UNIT_PRICE],item[DESCRIPTION])

#assign to slice
#할당시 순회가능한 객체 사용
l=list(range(10))
l[2:5]=[20,30]
print(l) #[0, 1, 20, 30, 5, 6, 7, 8, 9]. l[2:5]에 해당하는 [2,3,4](3항목)가 [20,30](2항목)으로 바뀌어 중간에 들어갔다
del l[5:7]
print(l) #[0, 1, 20, 30, 5, 8, 9]
l[3::2]=[11,22]
print(l) #[0, 1, 20, 11, 5, 22, 9]
#l[2:5]=100 #TypeError: can only assign an iterable
l[2:5]=[100]
print(l) #[0, 1, 100, 22, 9]