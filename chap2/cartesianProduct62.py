colors=['black','white']
sizes=['S','M','L']
tshirts=[(color,size) for color in colors for size in sizes] #앞의 것(color)가 뒤의 것(size)보다 나중에 순회됨
print(tshirts)
tshirts2=[(color,size) for size in sizes for color in colors] #비교용
print(tshirts2)