class MySeq:
	def __getitem__(self,index):
		return index

s=MySeq()
print(s[1]) # 1
print(s[1:4]) # slice(1, 4, None) #<-[]안 내용을 slice type으로 받는다
print(s[1:4:2]) # slice(1, 4, 2)
print(s[1:4:2,9]) # (slice(1, 4, 2), 9)
print(s[1:4:2,7:9]) # (slice(1, 4, 2), slice(7, 9, None))


print(slice) #<class 'slice'> #<-내장 자료형(내장 클래스)이다
print(dir(slice)) 
#['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', 
#'__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
#'__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'indices', 'start', 'step', 'stop']

#타 클래스엔 없는 특이 어트리뷰트: start, stop, step, indices
# help(slice.indices) #<-slice 처리용 기능임. 슬라이스 할 객체의 길이(len)를 받아 slice가 반환하는 튜플을 계산함
print(slice(None,10,2).indices(5)) #(0, 5, 2) #<-길이 5짜리 객체를 받아 [:10:2]를 했을때를 계산후 계산된 튜플을 돌려줌. [0:5:2]와 동일
print(slice(-3,None,None).indices(5)) #길이 5짜리 객체에서 (2, 5, 1). #<-[-3]은 [2,5,1]과 동일
#기반 시퀀스가 제공하는 서비스에 의존할 수 없을 때 슬라이스를 구현할 경우 이 메소드를 잘 이용할 것


