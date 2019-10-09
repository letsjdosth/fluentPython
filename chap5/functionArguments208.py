def tag(name,*content,cls=None,**attrs): #* 뒤의 키워드 인수는 절대로, 익명 위치인수로 전달되지 않는다.(죄다 *content에 들어가기 때문)
	"""generate a (or more) html tag """
	if cls is not None:
		attrs['class']=cls
	if attrs:
		attr_str=''.join(' %s="%s"'% (attr,value) for attr,value in sorted(attrs.items()))
	else:
		attr_str=''
	if content:
		return '\n'.join('<%s%s>%s</%s>'%(name,attr_str,c,name) for c in content)
	else:
		return '<%s%s />'%(name,attr_str)

print(tag('br')) #<br />
print(tag('p','hello')) #<p>hello</p>
print(tag('p','hello','world')) 
# <p>hello</p>
# <p>world</p>
print(tag('p','hello','world',cls='sidebar'))
# <p class="sidebar">hello</p>
# <p class="sidebar">world</p>
print(tag(content='testing',name='img')) 
#<img content="testing" /> #name은 인수이름대로 전달되었다. content는 *content가 아니라 **attr로 전달되었다. 위치인수 취급이 아니라 키워드인수 취급됨
my_tag={'name':'img','title':'Sunset Boulevard','src':'sunset.jpg','cls':'framed'}
print(tag(**my_tag)) 
#<img class="framed" src="sunset.jpg" title="Sunset Boulevard" /> #**를 붙이면 dict 안의 모든 항목을 별도의 인수로 전달. 인수 이름과 맞으면 해당 인수로, 아니면 **attrs


#가변개수 위치인수는 거부하며 키워드 인수를 지원하고 싶으면, 중간에 *를 넣을 것
def f(a,*,b):
	return a,b
print(f(1,b=2))
# print(f(1,2)) #TypeError: f() takes 1 positional argument but 2 were given. # *에 먹혀서 b가 지정되지 않는다
# print(f(1)) #TypeError: f() missing 1 required keyword-only argument: 'b'. b의 기본값이 없어서 필수로 b도 넘겨야 한다
