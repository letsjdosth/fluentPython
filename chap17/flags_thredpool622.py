from concurrent import futures

from flags620 import save_flag, get_flag, show, main

MAX_WORKERS=20

def download_one(cc):
	image=get_flag(cc)
	show(cc)
	save_flag(image, cc.lower()+'.gif')
	return cc

def download_many(cc_list):
	workers=min(MAX_WORKERS, len(cc_list))
	with futures.ThreadPoolExecutor(workers) as executor:
		res=executor.map(download_one, sorted(cc_list)) #내장 map과 비슷하다. 단, 스레드 executor가 생성한 스레드에 받은 함수를 리스트 요소의 인자로 동시에 뿌리는 것이 다르다. 리턴은 각 결과의 이터레이터이다.
	return len(list(res))

if __name__=='__main__':
	main(download_many)

# VN EG CN TR JP FR RU IN ID NGBRDE   PK MX BD ET PH CD US IR 
# 20 flags downloaded in 0.44s #<-14배 향상
# [Finished in 0.6s]