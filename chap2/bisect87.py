import bisect
import sys
import random

##ex1
HAYSTACK=[1,4,5,6,8,12,15,20,21,23,23,26,29,30]
NEEDLES=[0,1,2,5,8,10,22,23,29,30,31]

ROW_FMT='{0:2d} @ {1:2d}    {2}{0:<2d}'

def demo(bisect_fn):
	for needle in reversed(NEEDLES):
		position=bisect_fn(HAYSTACK,needle)
		offset=position*'  |'
		print(ROW_FMT.format(needle,position,offset))

if __name__=='__main__':
	if sys.argv[-1]=='left':
		bisect_fn=bisect.bisect_left #python bisect87.py left 같은 값일 때 왼쪽에 삽입
	else:
		bisect_fn=bisect.bisect #python bisect87.py 같은 값일 때 오른쪽에 삽입

print('DEMO:',bisect_fn.__name__)
print('haystack ->',' '.join('%2d'% n for n in HAYSTACK))
demo(bisect_fn)

#INSERT EXAMPLE (manually. insort보다 느림)
HAYSTACK.insert(14,31) #index,needle
HAYSTACK.insert(14,30)
HAYSTACK.insert(13,29)
print(HAYSTACK)



##ex2
def grade(score, breakpoints=[60,70,80,90],grades='FDCBA'):
	i=bisect.bisect(breakpoints,score)
	return grades[i]

print([grade(score) for score in [33,99,77,70,89,90,100]])



##ex3
size=7
random.seed(1729)
my_list=[]
for i in range(size):
	new_item=random.randrange(size*2)
	bisect.insort(my_list,new_item) #bisect.insort(seq,item) seq를 오름차순으로 유지한 채로 item을 seq에 삽입
	print('%2d ->' % new_item, my_list)
#insort_left()도 있음
