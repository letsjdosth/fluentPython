#문제가 나는 예
class HauntedBus:
	def __init__(self,passengers=[]):
		self.passengers=passengers #<-self.passengers가 passengers의 별명이 된다
	def pick(self,name):
		self.passengers.append(name)
	def drop(self,name):
		self.passengers.remove(name)

bus1=HauntedBus(['Alice','Bill']) #<-self.passengers를 명시적으로 초기화하며 시작한다
print(bus1.passengers) #['Alice', 'Bill']
bus1.pick('Charlie')
bus1.drop('Alice')
print(bus1.passengers) #['Bill', 'Charlie'] #문제 없음

bus2=HauntedBus() #<-self.passengers를 기본값으로 시작한다
bus2.pick('Carrie')
print(bus2.passengers) #['Carrie']

bus3=HauntedBus()
print(bus3.passengers) #['Carrie'] #<-!!!!!!!!!!!
bus3.pick('Dave')

print(bus2.passengers) #['Carrie', 'Dave'] #<-!!!!!!!!
print(bus2.passengers is bus3.passengers) #True #<-!!!!!! 같은 참조이다! 같은 객체를 보고있다!
print(bus1.passengers) #['Bill', 'Charlie'] #문제 없음

#이유: 함수의 디폴트 값이 함수가 정의될 때(=모듈이 로딩될 때) 평가되고 그 이후 기본값은 함수 객체의 어트리뷰트가 되기 때문
#이후 여러번 호출 시 기본값을 재평가하지 않은 채 그냥 해당 어트리뷰트의 값을 가져다 쓴다

print(dir(HauntedBus.__init__)) #...,'__defaults__',...
print(HauntedBus.__init__.__defaults__) #(['Carrie', 'Dave'],) #<-빈 리스트가 아니다! 마지막 값이 들어가있다!
print(HauntedBus.__init__.__defaults__[0] is bus2.passengers) #True


#방어적 프로그래밍: 일반적으로 가변객체를 기본값으로 사용시 None을 대신 쓰고 밑에서 할당
class TwilightBus:
	def __init__(self,passengers=None): #<-None을 넣어두고
		if passengers is None:
			self.passengers=[] #<-빈 리스트를 할당하자
		else:
			self.passengers=passengers
	def pick(self,name):
		self.passengers.append(name)
	def drop(self,name):
		self.passengers.remove(name)

#문제2. 거꾸로 인자로 넘기는 원래 리스트 자체는 변경되지 않아야 한다면?
basketball_team=['Sue','Tina','Maya','Diana','Pat']
bus=TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team) #['Sue', 'Maya', 'Diana'] #<-버스에 태웠다고 팀에서 없어져버렸다!

#이유: 인수를 명시적으로 넘길 시, 또 self.passengers가 passengers의 별명이 되기 때문. 같은 객체를 참조하게 된다.
#가변객체이므로, 함수/메소드 안에서 변경하면 해당 참조 객체가 바뀌어버린다. 따라서 basketball_team에서 빠지게 됨

#방어적 프로그래밍 2: 가변객체 인수를 받으면 그의 사본을 만들자
class TeamBus:
	def __init__(self,passengers=None):
		if passengers is None:
			self.passengers=[]
		else:
			self.passengers=list(passengers) #<-사본을 만든다. (덩달아, 리스트가 아니면 리스트로 변환)
	def pick(self,name):
		self.passengers.append(name)
	def drop(self,name):
		self.passengers.remove(name)
basketball_team=['Sue','Tina','Maya','Diana','Pat']
bus=TeamBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team) #['Sue', 'Tina', 'Maya', 'Diana', 'Pat']

#필요에 따라, 함수/메소드가 가변인수를 받을 때에
#1. 기존 처리값을 저장해둘지, 아니면 매번 초기화할지
#2. 원래 객체를 변경할지, 아니면 사본을 가져다 처리할지
#의도에 맞게 작동하도록 할 것
