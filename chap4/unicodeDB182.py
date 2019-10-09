import unicodedata
import re

re_digit=re.compile(r'\d')

sample='1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'

for char in sample:
	print('U+%04x'%ord(char), #U+코드포인트. ord(char): 하나의 유니코드 문자를 나타내는 문자열이 주어지면 해당 문자의 유니코드 코드 포인트를 나타내는 정수를 돌려줍니다. 반대는 chr()
		char.center(6),
		're_dig' if re_digit.match(char) else '-     ', #re_digit 정규식과 일치하는 경우 re_dig 표시
		'isdig' if char.isdigit() else '-    ',
		'isnum' if char.isnumeric() else '-    ',
		format(unicodedata.numeric(char),'5.2f'),
		unicodedata.name(char),
		sep='\t')

#결과에서 보듯, re의 \d는 유니코드를 제대로 못 거름. 다 숫자지만, 2개만 숫자로 봄
#regex 모듈은 좀 나음.(위 예제에서는 똑같이 동작하지만..)