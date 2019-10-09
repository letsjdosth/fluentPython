l=['spam','spam','eggs','spam']
print(set(l))
print(list(set(l)))

#set
s={1}
print(type(s),s)
print(s.pop())
print(s) #set(). {}는 빈 dict

from dis import dis #disassembler
dis('{1}') #<-더 짧음. 더 빠름
dis('set([1])') #<-위보다 느림


#frozenset
fs=frozenset(range(10))
print(fs)


#setcomp
from unicodedata import name 
#name: unicode에서 문자명을 가져옴
#unicodedata.name(unichr[, default])
#Returns the name assigned to the Unicode character unichr as a string. If no name is defined, default is returned, or, if not given, ValueError is raised.

sComp={chr(i) for i in range(32,256) if 'SIGN' in name(chr(i),'')}
print(sComp)
