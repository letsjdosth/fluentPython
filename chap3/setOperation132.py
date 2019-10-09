s={1,2,3,4,5,6,7,8,9,10}
z={5,6,7,8,9,10,11,12,13,14}

print(s&z, s.intersection(z))
print(s|z, s.union(z))
print(s-z, s.difference(z))
print(s^z, s.symmetric_difference(z))

print(s.isdisjoint(z)) #False


ss={1,2,3,4}
print(s>=ss)
print(s>ss)
print(s<=ss)
print(s<ss)
