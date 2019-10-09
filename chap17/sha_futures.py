#SHA-256 해시

import sys
import time
import hashlib #<-해시알고리즘을 가져다 쓸 것이다..
from concurrent import futures
from random import randrange

JOBS=12
SIZE=2**20
STATUS='{} workers, elapsed time:{:.2f}s'

def sha(size):
	data=bytearray(randrange(256) for i in range(size))
	algo=hashlib.new('sha256')
	algo.update(data)
	return algo.hexdigest()

def main(workers=None):
	if workers:
		workers=int(workers)
	t0=time.time()

	with futures.ProcessPoolExecutor(workers) as executor:
		actual_workers=executor._max_workers
		to_do=(executor.submit(sha,SIZE) for i in range(JOBS))
		for future in futures.as_completed(to_do):
			res=future.result()
			print(res)

	print(STATUS.format(actual_workers,time.time()-t0))

if __name__=='__main__':
	if len(sys.argv)==2:
		workers=int(sys.argv[1])
	else:
		workers=None
	main(workers)

#12코어 사용
# 89ce2da65093bcb3530851380d6a26e88eb04d85a0f4672414d83181d1490abf
# 8461460552842295966f545f635cbc47a723eb962ab6ba9e6a0d6d6db734a825
# fc216e6cacf191961b21fbf09fbe6fa9a6e6bb482fb5223303b5bab0d6065ca6
# d5827226112bacea13ff25775c6e399f070d324cb2db34cfa6002f0c730a58ca
# 3a4d220c95361a23574c72316209255d5fd95d2df32c6856b61ce7dacfa24aea
# 05b8b97bee6a0d5e36c1c5ff0644b52f28d0ecdf162523314ff9040987f98894
# 5bfabbb72524f7375e6b8ba7274c9daf0c0a2fc894d6d012dda4ae1b0a5246a4
# 4773af8d46179cb486eaf8157300a306d06ea428e5feaa35bb9ec2caebb6517d
# 76a44bbe8eca39b357dde68628e8a97fd7ca8199728a26b9857191629e9bb5e7
# 36f33b529b7aa8247abb1a09886af49d0cb5ef9e99fdc80bd93e1aa85caf5702
# 73ad056a24b667d8f28594154f89addac9dd891e02e3d35e90438fd8852290d6
# 5a2456ab638fd36b7a8d2e04096761fd8a60145892522239e86543e8f33d0283
# 12 workers, elapsed time:2.04s

#1코어 사용
# d00272ea60d9d79ff6deb00a648935d15ba9b90a8b7b12a0b0b7adf81c8ab0ea
# 34edeaa2d27c4c9f89b34e6be2777f62198902578bfc84e37a3344210d5d2453
# 8fe4f49e96d943859b0e3b86721932d67d402624923ee778fa36a8708dda2bc1
# 190f329e5fba7d9d66d3a1ca561566e791f1cdd7734be4f0aa019c80c792a1bc
# b2c6440e102c742d769fdeff5de2b00ec29570f5e993b5d2522d9ee9359032b5
# d887c81a8c738f8f7da3e61bfad0d7271618e43995ba87f0294ff297bdfb36b2
# 953b17b2decc1c3ad76579cec9c66192940e1e9241df2442475836ff210247bb
# a53acde6a8ff6eda65799c211e259496dd5229d89988c144518345f12edc762e
# 097b979514744a871d21e631377362c48f8bcb73f233e0366fa6fda4d615dccb
# ad66cac7c352b1f1149de2affeceb0f34f6e5b61cc730671d8fe3ca8d48444d2
# 71f94f605c023b80538a1d86a4383cd40a6c1b1883e0d543286b19ec43ab927b
# d751ca4203559122df6b6cb29b522b296663719e8849d83ab3da3481843cf944
# 1 workers, elapsed time:11.19s