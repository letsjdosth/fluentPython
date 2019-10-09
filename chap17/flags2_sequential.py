import collections

import requests
import tqdm

from flags2_common import main, save_flag, HTTPStatus, Result

DEFAULT_CONCUR_REQ=1 #기본동시요청수
MAX_CONCUR_REQ=1 #최대동시요청수

def get_flag(base_url, cc):
	#국기 url 접근 후 실제 다운로드 함수 (저장은 download_one에서 한다)
	url='{}/{cc}/{cc}.gif'.format(base_url,cc=cc.lower())
	resp=requests.get(url)
	if resp.status_code !=200:
		resp.raise_for_status() #200(정상)이 아니면 예외를 낸다
	return resp.content

def download_one(cc, base_url, verbose=False):
	try:
		image=get_flag(base_url, cc)
	except requests.exceptions.HTTPError as exc:
		res=exc.response
		if res.status_code==404: #get_flag에서 올라온 예외 중 404 만 예외처리하자.
			status=HTTPStatus.not_found
			msg='not found'
		else:
			raise
	else:
		save_flag(image, cc.lower()+'.gif')
		status=HTTPStatus.ok
		msg='OK'

	if verbose:
		print(cc, msg)

	return Result(status, cc)

#download_many_sequential. 동시처리와 비교하기 위한 비동시처리 케이스
def download_many(cc_list, base_url, verbose, max_req):
	counter=collections.Counter() #HttpStatus.~ (ok/not_found/error)의 합계를 각각 구하도록 카운터를 사용한다
	cc_iter=sorted(cc_list)
	if not verbose:
		cc_iter=tqdm.tqdm(cc_iter) #tqdm()은 움직이는 진행 막대를 보여주며, cc_iter에 들어있는 항목을 생성하는 반복자를 반환한다.
	for cc in cc_iter:
		try:
			res=download_one(cc, base_url, verbose) #get_flag에서 download_one을 거쳐 올라온 나머지 예외를 처리하자.
		except requests.exceptions.HTTPError as exc: #HTTP관련 예외를 잡는다
			error_msg='HTTP error {res.status_code}-{res.reason}'
			error_msg=error_msg.format(res=exc.response)
		except requests.exceptions.ConnectionError as exc: #기타 네트워크 관련 예외를 잡는다
			error_msg='Connection error'
		else:
			error_msg=''
			status=res.status #여기까지 모두 문제가 없었다면 status에 HTTPStatus.ok가 들어간다 (download_one 참고)

		if error_msg:
			status=HTTPStatus.error #문제가 있었다면, status에 HTTPStatus.error가 들어간다.
		counter[status]+=1 #<-status를 보고, 그를 counter의 key로 사용해서 해당 value을 하나 증가시킨다
		if verbose and error_msg:
			print('*** Error for {}: {}'.format(cc, error_msg))
	return counter

if __name__=='__main__':
	main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

# 결과 예시
# Searching for 20 flags: from LOCAL to http://localhost:8001/flags
# 1 concurrent connection will be used.

#   0%|          | 0/20 [00:00<?, ?it/s]
#   5%|▌         | 1/20 [00:01<00:19,  1.02s/it]
#  10%|█         | 2/20 [00:02<00:18,  1.02s/it]
#  15%|█▌        | 3/20 [00:03<00:17,  1.02s/it]
#  20%|██        | 4/20 [00:04<00:16,  1.02s/it]
#  25%|██▌       | 5/20 [00:05<00:15,  1.02s/it]
#  30%|███       | 6/20 [00:06<00:14,  1.02s/it]
#  35%|███▌      | 7/20 [00:07<00:13,  1.02s/it]
#  40%|████      | 8/20 [00:08<00:12,  1.02s/it]
#  45%|████▌     | 9/20 [00:09<00:11,  1.02s/it]
#  50%|█████     | 10/20 [00:10<00:10,  1.02s/it]
#  55%|█████▌    | 11/20 [00:11<00:09,  1.02s/it]
#  60%|██████    | 12/20 [00:12<00:08,  1.02s/it]
#  65%|██████▌   | 13/20 [00:13<00:07,  1.02s/it]
#  70%|███████   | 14/20 [00:14<00:06,  1.02s/it]
#  75%|███████▌  | 15/20 [00:15<00:05,  1.02s/it]
#  80%|████████  | 16/20 [00:16<00:04,  1.02s/it]
#  85%|████████▌ | 17/20 [00:17<00:03,  1.01s/it]
#  90%|█████████ | 18/20 [00:18<00:02,  1.01s/it]
#  95%|█████████▌| 19/20 [00:19<00:01,  1.01s/it]
# 100%|██████████| 20/20 [00:20<00:00,  1.01s/it]
# --------------------
# 20 flags downloaded.
# Elapsed time: 20.33s
# [Finished in 20.5s]