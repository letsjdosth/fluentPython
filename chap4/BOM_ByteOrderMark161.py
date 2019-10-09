#little endian: 코드 포인트의 최하위 포인트가 먼저 나옴 (인텔)
#big endian: 코드 포인트의 최상위 포인트가 먼저 나옴 (IBM)

u16='El Niño'.encode('utf_16')
print(u16) 
#b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'
#utf-16의 앞 2바이트 \xff\xfe는 Byte Order Mark. 리틀앤디언-빅앤디언을 확인하기 위해 UTF16 인코더가 추가함
#U+FEFF (ZERO WIDTH NO-BREAK SPACE)(리틀앤디언 컴퓨터에서는 255,254에 해당)는 화면에 출력되지 않음.
#빅앤디언에서는 U+FFFE로 읽으나, 이에 해당하는 utf-16의 글자는 없음
#거꾸로 빅앤디언 컴퓨터에서 utf-16으로 인코딩된 바이트열의 경우, 첫 2바이트가 \xfe\xff가 되고, 리틀엔디언 컴퓨터에서는 없는 글자가 됨

#참고: UTF16의 표준은 빅앤디언임.

print(list(u16)) #little endian

#utf-16le: 리틀앤디언 명시 코덱 (BOM 생성 안 함)
#utf-16be: 빅엔디언 명시 코덱 (BOM 생성 안 함)
u16le='El Niño'.encode('utf_16le')
print(list(u16le))
u16be='El Niño'.encode('utf-16be')
print(list(u16be))