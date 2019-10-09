#다중 스레드가 아니라 다중 프로세스를 이용해 GIL을 우회해보자

import os
from concurrent import futures

from flags620 import save_flag, get_flag, show, main

MAX_WORKERS=20

def download_one(cc):
	image=get_flag(cc)
	show(cc)
	save_flag(image, cc.lower()+'.gif')
	return cc

def download_many(cc_list):
	with futures.ProcessPoolExecutor() as executor: #<-스레드가 아니라 프로세스. 프로세스 수는 기본적으로 os.cpu_count()의 반환값을 사용하므로, 보통은 별도로 설정하지 않아도 된다.
		res=executor.map(download_one, sorted(cc_list))
	return len(list(res))

if __name__=='__main__':
	print(os.cpu_count()) #12
	main(download_many)

# BR ID IN FR CN EG JP DE BD ET CD IR NG RU PK TR VN MX PH US 
# 20 flags downloaded in 1.12s 
# [Finished in 2.0s]
#<-스레드보다 느려졌다. 기존 스레드 수(20)보다 cpu 코어 수(12)가 적어서 그런 듯. 
#스레드는 물리적인 제약 없이 엄청 많이(~수천) 생성 가능하기 때문에 I/O 바운드에 걸리는 작업은 스레드로 하자

