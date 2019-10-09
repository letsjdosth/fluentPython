fruits=['grape','raspberry','apple','banana']

print(sorted(fruits))
print(fruits)
print(sorted(fruits,reverse=True))
print(sorted(fruits,key=len)) #not len()
print(sorted(fruits,reverse=True,key=len))
print(fruits) #sorted()는 새로 만들어 반환하므로 기존 객체는 그대로 있다
fruits.sort()
print(fruits) #.sort()는 해당 리스트를 변화시켜 반환