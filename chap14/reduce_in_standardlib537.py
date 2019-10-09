#반복형을 리듀스(=폴딩=누적)하는 함수
#반복형->값 (1개)

#사실 모두 functools.reduce()로 구현 가능하지만, 그 중 자주 쓰는 유형을 내장형으로 만들어 둠
#또한 all/any는 reduce()로 짜는것보다 효율적임

#functools.reduce(func, it, [initial]) #func는 리턴값이 있는 인수 2개짜리 함수 #higherOrderFunc199.py 참고

#all(it) : it의 모든 요소가 참이면 True, 아니면 False
assert all([]) #<-!!언제나 True
assert all([1,2,3])
assert not all([1,0,3])

#any(it) : it의 하나라도 참이면 True, 아니면 False
assert not any([]) #<-언제나 False
assert any([1,2,3])
assert any([1,0,3])
assert not any([0,0,0])

g=(n for n in [0,0.0,7,8])
print(any(g)) #True
print(next(g)) #8 #<-에러가 안나고 8이 나온다. 이는 any가 True를 확신하는 순간 next() 호출을 중지하기 때문. (short circuit evaluation)

h=(n for n in [1,4,0,7,9])
print(all(h)) #False
print(next(h)) #7 #<-마찬가지이다

#~easy~
#max(it[, key=][,default=]) 혹은 max(arg1,arg2,...,[key=?]) 최대값. key는 인수 1개짜리 콜러블이며 평가기준으로 사용된다(key(args)의 최대값을 구하게 됨. it이 비면 default가 반환된다)
#min(it[, key=][,default=]) 혹은 min(arg1,arg2,...,[key=?]) 최소값
#sum(it,start=0) #<-start 값은 합계 계산 시 더하면서 시작한다

