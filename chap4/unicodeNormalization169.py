s1='café'
s2='cafe\u0301' #U+0301: COMBINING ACUTE ACCENT #unicode 표준에서는: 규범적으로 동일하다. 애플리케이션은 동일하게 처리해야
print(s1,s2) #café café
print(len(s1),len(s2)) #4 5
print(s1==s2) #False #파이썬은 다르게 처리함-_-

from unicodedata import normalize, name

#normalize의 첫 인수: 'NFC', 'NFD', 'NFKC', 'NFKD'. 각각 정규화하는 방식이 다름
print(len(normalize('NFC',s1)),len(normalize('NFC',s2))) #4,4 #NFC:가장 짧은 동일 문자열
print(len(normalize('NFD',s1)),len(normalize('NFD',s2))) #5,5 #NFD:조합 문자 분리

#NFC가 웹 등을 위한 추천 형식임. 단, NFC 문자열 청소 시 원래 다른 글자였던 것으로 바뀌는경우도 있음
ohm='\u2126'
print(name(ohm)) #OHM SIGN
ohm_c=normalize('NFC',ohm)
print(name(ohm_c)) #GREEK CAPITAL LETTER OMEGA
print(ohm==ohm_c) #False #-_-
print(normalize('NFC',ohm)==normalize('NFC',ohm_c)) #True



#~K~: compatibility. 호환성 문자에 영향(유니코드에, 기존 표준과의 호환성을 위해 2번이상 나타나는 문자)
print('\u00B5',name('\u00B5')) #µ MICRO SIGN (latin1과의 상호변환을 위해 추가)
print('\u03BC',name('\u03BC')) #μ GREEK SMALL LETTER MU1

half='\u00BD'
print(half,normalize('NFKC',half)) #½ 1⁄2

# four_squared='42'
# print(four_squared,normalize('NFKC',four_squared)) #42 42

micro='\u00B5'
print(micro,normalize('NFKC',micro)) #µ μ
print(ord(micro),ord(normalize('NFKC',micro))) #181 956
#단, NFKC, NFKD는 데이터의 의미 자체를 바꾸는 변환을 할 수도 있음. 검색/색인을 위한 중간단계로만 사용





#case folding : 모든 텍스트를 소문자로(str.lower()). 단, 약간 변환하는 경우가 있음(unicode의 0.11%, 116 코드포인트)
#str.casefold()

micro='\u00B5'
print(name(micro)) #MICRO SIGN
micro_cf=micro.casefold()
print(name(micro_cf)) #GREEK SMALL LETTER MU
print(micro,micro_cf) #µ μ


eszett='ß'
print(name(eszett)) #LATIN SMALL LETTER SHARP S
eszett_cf=eszett.casefold()
print(eszett,eszett_cf) #ß ss

