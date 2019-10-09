import collections
from concurrent import futures

import requests
import tqdm

from flags2_common import main, HTTPStatus
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ=30 #기본동시요청수
MAX_CONCUR_REQ=1000 #최대동시요청수

def download_many(cc_list, base_url, verbose, concur_req):
	counter=collections.Counter() #마찬가지로 Counter()를 이용해 ok/error 수를 센다.
	with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:
		to_do_map={} 
		#해당 퓨처가 어떤 국가의 국기에 해당하는것인지 나중에(우리는.. 오류 보고에 사용할 것임) 꺼내오기 위한 dict 
		#<-이 dict는 threadpoolexecutor가 도는데 필수적인 요소는 아니다. 하지만 관용구처럼 함께 쓰인다. 스레드가 임의의 순서로 완료되더라도, 다시 매핑을 통해 매칭해 처리하기 쉽기 때문.

		for cc in sorted(cc_list):
			future=executor.submit(download_one, cc, base_url, verbose)
			to_do_map[future]=cc #<-여기서 future에 국기를 매칭해 넣는다
		done_iter=futures.as_completed(to_do_map) #<-각 작업이 완료되는대로 Futures 객체를 반환하는 제너레이터.
		if not verbose:
			done_iter=tqdm.tqdm(done_iter, total=len(cc_list))
		for future in done_iter: #<-여기에서 작업완료대기 등의 블로킹이 걸리므로, 아래는 코드는 시작되기만 하면 바로 실행된다.
			try:
				res=future.result() #<-예외처리를 result()에서 한다. result()가 콜러블이 반환한 값이나 콜러블을 실행하는 동안 잡은 예외를 재발생시키기 때문 (as_competed에서가 아니다!)
			except requests.exceptions.HTTPError as exc: #HTTP관련 에러(단, 400은 download_one에서 미리 처리된다)
				error_msg='HTTP {res.status_code} - {res.reason}'
				error_msg=error_msg.format(res=exc.response)
			except requests.exceptions.ConnectionError as exc: #네트워크 연결관련 에러
				error_msg='Connection error'
			else:
				error_msg=''
				status=res.status #여기까지 예외가 하나도 나지 않으면, 그대로 status를 가져오고 HTTPStatus.ok가 된다.
			if error_msg: #하나라도 예외가 나면 error_msg가 ''가 아니게 되어 True가 된다.
				status=HTTPStatus.error
			counter[status]+=1 #현 status에 맞는 Counter의 status 항목에 1을 더한다
			if verbose and error_msg:
				cc=to_do_map[future] #<-여기서 future에 해당하는 국기를 가져와 오류 보고 메시지를 만든다
				print('*** Error for {}: {}'.format(cc,error_msg))
	return counter

if __name__=='__main__':
	main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

#결과 예시
# Searching for 20 flags: from LOCAL to http://localhost:8001/flags
# 20 concurrent connections will be used.

#   0%|          | 0/20 [00:00<?, ?it/s]
#   5%|▌         | 1/20 [00:01<00:19,  1.00s/it]
# 100%|██████████| 20/20 [00:01<00:00, 19.62it/s]
# --------------------
# 20 flags downloaded.
# Elapsed time: 1.05s
# [Finished in 1.3s]