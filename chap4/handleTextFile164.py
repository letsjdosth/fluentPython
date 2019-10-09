fp=open('cafe.txt','w',encoding='utf_8')
print(fp) #<_io.TextIOWrapper name='cafe.txt' mode='w' encoding='utf_8'>
print(fp.write('café')) #4 =>유니코드 문자 수 반환
fp.close()


print(open('cafe.txt').read()) #caf챕 #encoding을 지정하지 않으면 시스템 기본 인코딩(윈도우의 것)을 이용함
import os
print(os.stat('cafe.txt').st_size) #5 (!!!!!) =>5byte기 때문. 아래 fp4에서 보듯, 5바이트로 인코딩되었기 떄문


fp2=open('cafe.txt') 
print(fp2) #<_io.TextIOWrapper name='cafe.txt' mode='r' encoding='cp949'>
print(fp2.encoding) #cp949
print(fp2.read())
fp2.close()

fp3=open('cafe.txt',encoding='utf_8')
print(fp3)
print(fp3.read()) #<_io.TextIOWrapper name='cafe.txt' mode='r' encoding='utf_8'>
fp3.close() #café

fp4=open('cafe.txt','rb')
print(fp4) #<_io.BufferedReader name='cafe.txt'> #binary 모드는 객체가 다름
print(fp4.read()) #b'caf\xc3\xa9'