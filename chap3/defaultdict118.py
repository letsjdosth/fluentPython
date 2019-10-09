import sys
import re
import collections

WORD_RE=re.compile(r'\w+') #\w: [a-zA-Z0-9], +:1개이상 
index=collections.defaultdict(list) #defaultdict는 key가 없으면 인수값(지금은 빈 list)을 value로 가진 key를 생성함

with open('zen.txt', encoding='utf-8') as fp:
	for line_no, line in enumerate(fp,1):
		for match in WORD_RE.finditer(line): 
			word=match.group()
			column_no=match.start()+1
			location=(line_no,column_no)
			index[word].append(location) 

for word in sorted(index,key=str.upper):
	print(word, index[word])
