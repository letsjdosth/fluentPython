import sys
import re

WORD_RE=re.compile(r'\w+') #\w: [a-zA-Z0-9], +:1개이상 
index={}

with open('zen.txt', encoding='utf-8') as fp:
	for line_no, line in enumerate(fp,1):
		for match in WORD_RE.finditer(line): 
			#finditer(): 정규식과 매치되는 모든 문자열(substring)을 iterator 객체(Match object)로 리턴
			word=match.group() #group(): 문자열(string)로 반환
			column_no=match.start()+1
			location=(line_no,column_no)

			# occurrences=index.get(word,[]) #dict.get(k,new):dict[k]가 있으면 가져옴. 없으면 new를 리턴
			# occurrences.append(location)
			# index[word]=occurrences
			index.setdefault(word,[]).append(location) #위를 한줄로. 
			#dict.setdefault(k,default): key k가 있으면 dict[k]를 리턴. 없으면 dict[k]=default로 설정해 리턴

for word in sorted(index,key=str.upper):
	print(word, index[word])
