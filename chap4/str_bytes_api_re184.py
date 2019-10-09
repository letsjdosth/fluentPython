import re
#re는 이중 모듈. bytes/str을 모두 받을 수 있음 (받기는 다 받는데 다르게 동작함)

re_numbers_str=re.compile(r'\d+')
re_words_str=re.compile(r'\w+')
re_numbers_bytes=re.compile(rb'\d+')
re_words_bytes=re.compile(rb'\w+')

text_str=("Ramanujan saw \u0b27\u0bed\u0be8\u0bef as 1729 = 1³ + 12³ = 9³ + 10³.") #타밀숫자 1729
text_bytes=text_str.encode('utf_8')

print('Text',repr(text_str),sep='\n  ')
print('Numbers')
print('  str  :',re_numbers_str.findall(text_str))
print('  bytes:',re_numbers_bytes.findall(text_bytes))
print('Words')
print('  str  :',re_words_str.findall(text_str))
print('  bytes:',re_words_bytes.findall(text_bytes))
'''
Text
  'Ramanujan saw ଧ௭௨௯ as 1729 = 1³ + 12³ = 9³ + 10³.'
Numbers
  str  : ['௭௨௯', '1729', '1', '12', '9', '10']  #<-타밀 숫자에도 매칭
  bytes: [b'1729', b'1', b'12', b'9', b'10'] #<-바이트는 못함. 아스키에만 매칭
Words
  str  : ['Ramanujan', 'saw', 'ଧ௭௨௯', 'as', '1729', '1³', '12³', '9³', '10³'] #<-문자, 위첨자, 타밀, 아스키 모두
  bytes: [b'Ramanujan', b'saw', b'as', b'1729', b'1', b'12', b'9', b'10'] #<-문자, 숫자에 대한 아스키 바이트에만
'''

#결론: bytes 정규식은 ascii 매칭만
#(str 정규식도 ascii 매칭만 하도록 하는 re.ASCII 플래그가 있음)