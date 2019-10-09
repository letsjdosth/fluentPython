#functools.partial(func,args...) : 함수를 부분적으로 실행. 원 함수의 일부 인수를 고정한 callable 생성
#뒤 인수는 keyword 인수일 경우 키워드 및 바인딩 값 줄 것 (keyword1=value1). 그냥 ,로 구분하며 넣으면 위치인수에 차례대로 들어감
#(callback func api에서 유용)

from operator import mul
from functools import partial

triple=partial(mul,3) #mul(3,arg)로 고정
print(triple(7)) #21
print(list(map(triple,range(1,10)))) #[3, 6, 9, 12, 15, 18, 21, 24, 27] #참고: map은 인수 하나짜리 함수만 받는다


import unicodedata, functools
nfc=functools.partial(unicodedata.normalize,'NFC') #normalize('NFC',arg)로 고정
s1='café'
s2='cafe\u0301' #\u0301: 앞글자에 강세기호 결합
print(s1,s2,s1==s2) #café café False
print(nfc(s1)==nfc(s2)) #True


from functionArguments208 import tag
print(tag)
picture=partial(tag,'img',cls='pic-frame') #<function tag at 0x000002043AE26D90>
print(picture) #functools.partial(<function tag at 0x000002043AE26D90>, 'img', cls='pic-frame') 
print(picture(src='wumpus.jpeg')) #<img class="pic-frame" src="wumpus.jpeg" />
print(picture.func) #<function tag at 0x000002043AE26D90> #<-원래함수에 접근할 수 있는 속성을 들고 있다
print(picture.args) #('img',) #positional args #<-고정된 인수에 접근할 수 있는 속성을 들고 있다
print(picture.keywords) #{'cls': 'pic-frame'} #keyword args #<-고정된 인수에 접근할 수 있는 속성을 들고 있다(2)

#functools.partialmethod() : 클래스 메서드에 대해 작동하도록 설계됨. 나머진 partial과 같음

