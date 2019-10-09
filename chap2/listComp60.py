#참고
#chr: 유니코드 코드 포인트가 정수 i 인 문자를 나타내는 문자열을 돌려줍니다. 예를 들어, chr(97) 은 문자열 'a' 를 돌려주고, chr(8364) 는 문자열 '€' 를 돌려줍니다.
#ord: 하나의 유니코드 문자를 나타내는 문자열이 주어지면 해당 문자의 유니코드 코드 포인트를 나타내는 정수를 돌려줍니다. 예를 들어, ord('a') 는 정수 97 을 반환하고 ord('€') (유로 기호)는 8364 를 반환합니다. 

symbols=[chr(x) for x in [36,162,163,165,8364,164]]
print(symbols)
codes=[ord(x) for x in symbols]

print(codes)


beyond_ascii=[ord(s) for s in symbols if ord(s)>127] #map+filter를 이용한 작업을 다 할 수 있음
print(beyond_ascii)

beyond_ascii2=list(filter(lambda c: c>127, map(ord, symbols)))
print(beyond_ascii2)