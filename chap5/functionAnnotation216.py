#함수 선언부에 메타데이터 추가 가능
#매개변수에는 : 뒤에 표현식. 디폴트 값이 있을 때에는 인수명과 = 사이에 추가
#반환값에는 : ()과 : 사이에 ->표현식 으로 추가
#표현식에는 자료형 관계없이 아무거나 들어올 수 있음. 클래스(str,int,사용자정의class이름 등), 문자열 등

#function.__annotations__에 저장됨(dict형태)
#python interpreter는 이에 대해 아무것도 안 함 (검사 x 검증 x. 위 속성을 통해 IDE나 프레임워크, 데커레이터 등이 사용할 수 있긴 함)

def clip(text:str, max_len:'int>0'=80)->str:
	"""max_len 앞이나 뒤의 마지막 공백에서 뒤를 잘라낸 텍스트 반환"""
	end=None
	if len(text)>max_len:
		space_before=text.rfind(' ',0,max_len)
		if space_before>=0:
			end=space_before
		else:
			space_after=text.rfind('',max_len)
			if space_after>=0:
				end=space_after
	if end is None:
		end=len(text)
	return text[:end].rstrip() 

print(clip.__annotations__) #{'text': <class 'str'>, 'max_len': 'int>0', 'return': <class 'str'>}

from inspect import signature
sig=signature(clip)
print(sig.return_annotation) #<class 'str'>
print(sig.parameters) #OrderedDict([('text', <Parameter "text:str">), ('max_len', <Parameter "max_len:'int>0'=80">)])
for param in sig.parameters.values():
	note=repr(param.annotation).ljust(13)
	print(note,':',param.name,'=',param.default)
# <class 'str'> : text = <class 'inspect._empty'>
# 'int>0'       : max_len = 80