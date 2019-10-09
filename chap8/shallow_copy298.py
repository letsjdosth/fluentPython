
l1=[3,[55,44],(7,8,9)]
l2=list(l1) #<-사본을 생성한다
print(l2)
assert l2==l1
assert not l2 is l1 #<-다르다. 다른 객체를 참조한다

#하지만, 이는 얕은 복사임
l1.append(100)
l1[1].remove(55)
print('l1:',l1) #l1: [3, [44], (7, 8, 9), 100] #<-append는 l1 객체에 대한 메소드
print('l2:',l2) #l2: [3, [44], (7, 8, 9)] #<-55가 지워졌다. 
#이는 복제 시 최상위 컨테이너는 복제하나, 그 아래 들어있는 것은 동일 객체에 대한 참조로 채우기 때문
#즉, l1[1]과 l2[1]이 같은 참조를 가지고 있었어서 (즉 같은 객체를 보고 있었어서) 이런 일이 일어남

l2[1]+=[33,22] #l1: [3, [44, 33, 22], (7, 8, 9), 100]
l2[2]+=(10,11) #l2: [3, [44, 33, 22], (7, 8, 9, 10, 11)]
print('l1:',l1)
print('l2:',l2) 
#list는 가변 객체. += 연산 시 같은 참조의 리스트를 변경하므로, 참조가 동일한 채로 남아있고 따라서 l2도 바뀐다
#tuple은 불변 객체. += 연산 시 새로운 tuple을 만들어 반환하므로, 참조가 달라지고 따라서 기존 객체를 보고 있는 l1은 바뀌지 않느다
