from cardDeck39 import FrenchDeck
from random import shuffle

deck=FrenchDeck()
# shuffle(deck) #TypeError: 'FrenchDeck' object does not support item assignment
#할당을 지원하지 않음


#멍키패칭: 걍 실행중에 뜯어고치자 (콘솔에서 바로 가능). __setitem__만 있으면 됨
def set_card(deck,position,card): #deck은 self자리.(굳이 이름이 self여야 하는건 아니다. 관례상 self)
	deck._cards[position]=card

FrenchDeck.__setitem__=set_card #일급 객체!

shuffle(deck) #<-된다. 
print(deck[:5])
#1.프로토콜은 인수의 자료형엔 신경쓰지 않음. 동작하게 하는 메소드가 있으면 그만(덕 타이핑)
#2.프로토콜은 메서드를 원래 가지고 있던 것인지, 아니면 나중에 추가한 것인지도 신경쓰지 않음. 동적으로 작동(멍키패칭 가능)
