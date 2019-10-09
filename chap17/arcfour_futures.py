import sys
import time
from concurrent import futures
from random import randrange

from arcfour import arcfour

JOBS=12
SIZE=2**18

KEY=b'Twas brillig, and t he slithy toves\nDid gyre'
STATUS='{} workers, elapsed time:{:.2f}s'

def arcfour_test(size,key):
	in_text=bytearray(randrange(256) for i in range(size))
	cypher_text=arcfour(key, in_text)
	out_text=arcfour(key, cypher_text)
	assert in_text==out_text, 'Failed arcfour_test'
	return size

def main(workers=None):
	if workers:
		workers=int(workers)
	t0=time.time()
	with futures.ProcessPoolExecutor(workers) as executor:
		actual_workers=executor._max_workers
		to_do=[]
		for i in range(JOBS,0,-1):
			size=SIZE+int(SIZE/JOBS*(i-JOBS/2))
			job=executor.submit(arcfour_test,size,KEY) 
			#참고: submit(fn, *args, **kwargs) 
			#Schedules the callable, fn, to be executed as fn(*args **kwargs) and returns a Future object representing the execution of the callable.
			to_do.append(job)
		for future in futures.as_completed(to_do):
			res=future.result()
			print('{:.1f} KB'.format(res/2**10))
	print(STATUS.format(actual_workers, time.time()-t0))

if __name__=='__main__':
	if len(sys.argv)==2:
		workers=int(sys.argv[1])
	else:
		workers=None
	main(workers)

#12코어 사용
# 149.3 KB
# 170.7 KB
# 192.0 KB
# 213.3 KB
# 234.7 KB
# 256.0 KB
# 277.3 KB
# 298.7 KB
# 320.0 KB
# 362.7 KB
# 384.0 KB
# 341.3 KB
# 12 workers, elapsed time:1.29s

#1코어 사용
# 384.0 KB
# 362.7 KB
# 341.3 KB
# 320.0 KB
# 298.7 KB
# 277.3 KB
# 256.0 KB
# 234.7 KB
# 213.3 KB
# 192.0 KB
# 170.7 KB
# 149.3 KB
# 1 workers, elapsed time:6.54s
# [Finished in 6.6s]