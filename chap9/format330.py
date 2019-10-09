# format(value[, format_spec])
# Convert a value to a “formatted” representation, as controlled by format_spec. #<-format_spec: 포맷 명시자 로 번역
# The interpretation of format_spec will depend on the type of the value argument, #<-중요! 포맷 명시자를 value type에 따라(즉, 해당 클래스가) 원하는 방식으로 해석할 수 있음
# however there is a standard formatting syntax that is used by most built-in types: Format Specification Mini-Language. #<-스탠다드 포맷팅 문법: 포맷 명시 간이 언어 로 번역

'''
포맷 명시 간이 언어 문서: https://docs.python.org/3/library/string.html#formatspec
format_spec     ::=  [[fill]align][sign][#][0][width][grouping_option][.precision][type]
fill            ::=  <any character>
align           ::=  "<" | ">" | "=" | "^" (좌측정렬|우측정렬|숫자에서 부호와 숫자사이 패딩|가운데정렬)
sign            ::=  "+" | "-" | " " (양수에도+부호강제|음수에만부호붙이고양수엔안붙임(디폴트)|양수는빈칸음수는부호)
#               ::= alternate form. int/float/decimal/complex에만 해당. 타입에 따라 다르게 정의되어 있음. int의 경우 0b(2진수),0o(8진수),0x(16진수) 등)
width           ::=  digit+ (최소필드폭)
grouping_option ::=  "_" | "," (thousands saparator. _는 _가 있으며 추가 요소(X 등)로 4digit당 구분자도 만들 수 있음)
precision       ::=  digit+ (10진수에서 몇자리까지 정확히 표시할지. f:소수점 뒤 몇자리 g:소수점 전 몇자리. 값이 10진수가 아닌경우 최대필드폭)
type            ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"
	for string
		's':String format. This is the default type for strings and may be omitted.
		None:The same as 's'.
	for integer
		'b':Binary format. Outputs the number in base 2.
		'c':Character. Converts the integer to the corresponding unicode character before printing.
		'd':Decimal Integer. Outputs the number in base 10.
		'o':Octal format. Outputs the number in base 8.
		'x':Hex format. Outputs the number in base 16, using lower-case letters for the digits above 9.
		'X':Hex format. Outputs the number in base 16, using upper-case letters for the digits above 9.
		'n':Number. This is the same as 'd', except that it uses the current locale setting to insert the appropriate number separator characters.
		None:The same as 'd'.
	for float
		'e':Exponent notation. Prints the number in scientific notation using the letter ‘e’ to indicate the exponent. The default precision is 6.
		'E':Exponent notation. Same as 'e' except it uses an upper case ‘E’ as the separator character.
		'f':Fixed-point notation. Displays the number as a fixed-point number. The default precision is 6.
		'F':Fixed-point notation. Same as 'f', but converts nan to NAN and inf to INF.
		'g':General format. For a given precision p >= 1, this rounds the number to p significant digits and then formats the result in either fixed-point format or in scientific notation, 
			depending on its magnitude.
			The precise rules are as follows: suppose that the result formatted with presentation type 'e' and precision p-1 would have exponent exp. 
			Then if -4 <= exp < p, the number is formatted with presentation type 'f' and precision p-1-exp.
			Otherwise, the number is formatted with presentation type 'e' and precision p-1. 
			In both cases insignificant trailing zeros are removed from the significand, and the decimal point is also removed if there are no remaining digits following it.
			Positive and negative infinity, positive and negative zero, and nans, are formatted as inf, -inf, 0, -0 and nan respectively, regardless of the precision.
			A precision of 0 is treated as equivalent to a precision of 1. The default precision is 6.
		'G':General format. Same as 'g' except switches to 'E' if the number gets too large. The representations of infinity and NaN are uppercased, too.
		'n':Number. This is the same as 'g', except that it uses the current locale setting to insert the appropriate number separator characters.
		'%':Percentage. Multiplies the number by 100 and displays in fixed ('f') format, followed by a percent sign.
		None:Similar to 'g', except that fixed-point notation, when used, has at least one digit past the decimal point. 
			The default precision is as high as needed to represent the particular value. The overall effect is to match the output of str() as altered by the other format modifiers.

'''

brl=1/2.43
print(brl)
#format() 사용 예
print(format(brl,'0.4f')) #<-두번째 인자로 (포맷명시간이언어로 된)포맷 명시자가 들어온다
#str.format() 사용 예
print('1 BRL= {rate:0.2f} USD'.format(rate=brl)) #'{필드명:포맷 명시자}'.format(필드와의 맵핑)


print(format(42,'b')) #101010 #int의 b이므로 2진수로 바뀐다
print(format(2/3,'.1%')) #66.7% #float의 %이므로 퍼센트로 바뀐다. 소수점 뒤 1자리까지 표시한다



#포맷 명시자 자체 해석 예
from datetime import datetime
now=datetime.now()
print(format(now,'%H:%M:%S')) #19:18:34 #<-이건 표준 포맷명시 간이언어가 아님. datetime 모듈 클래스에서 자체 정의한 것임. __format__()을 정의하면 됨
print("It's now {:%I:%M %p}".format(now)) #It's now 07:18 PM

from vector2d_v1_328 import Vector2d #<- __format__()이 정의되어있지 않음. 이럴 경우 기본으로 object에서 상속받은 메서드가 str(my_object)를 반환한다.
v1=Vector2d(3,4)
format(v1) #(3.0, 4.0) #<-str(v1), 즉 __str__이 정의된 대로 나옴
try:
	format(v1,'.3f') #<-받을 수 없는 포맷 명시자를 넘기면
except TypeError as e:
	print(e) #unsupported format string passed to Vector2d.__format__ #<-에러난다

