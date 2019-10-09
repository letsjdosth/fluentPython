import doctest

from tombola412 import Tombola

import bingo417, lotto418, tombolist420

TEST_FILE='tombola_test.rst'
TEST_MSG='{0:16} {1.attempted:2} tests, {1.failed:2} failed - {2}'

def main(argv):
	verbose='-v in argv'
	real_subclasses=Tombola.__subclasses__()
	#__subclasses__메모리에 살아있는 직속 서브클래스 나열. 이 때문에 실제 코드에서는 직접 사용하지 않아도 서브클래스들을 임포트한 것임
	virtual_subclasses=list(Tombola._abc_registry)
	#_abc_registry: abc의 어트리뷰트. 추상 클래스의, 등록된 가상 서브클래스에 대한 약한 참조를 가지고있는 WeakSet

	printed_msg=[]
	for cls in real_subclasses+virtual_subclasses:
		printed_msg.append(test(cls,verbose)) #test함수를 실행한 후에 그 리턴을 메시
	
	print('***total result***')
	for msg in printed_msg:
		print(msg)

def test(cls, verbose=False):
	res=doctest.testfile(
		TEST_FILE,
		globs={'ConcreteTombola':cls},
		verbose=verbose,
		optionflags=doctest.REPORT_ONLY_FIRST_FAILURE) #<-doctest.REPORT_ONLY_FIRST_FAILURE가 제대로 먹고 있는건지 확인 필요
	tag='FAIL' if res.failed else 'OK'
	
	msg=TEST_MSG.format(cls.__name__,res,tag)
	print(msg)
	return msg

if __name__=='__main__':
	import sys
	main(sys.argv)
