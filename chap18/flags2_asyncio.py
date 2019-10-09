import asyncio
import collections
import aiohttp
from aiohttp import web
import tqdm

from flags2_common import main, HTTPStatus, Result, save_flag

#오류방지를 위한 낮은 기본값 설정
DEFAULT_CONCUR_REQ=5
MAX_CONCUR_REQ=1000

class FetchError(Exception): #국가코드를 가지고있는 예외 클래스(예외 래핑 클래스) 정의
	def __init__(self, country_code):
		self.country_code=country_code

async def get_flag(base_url,cc):
	url='{}/{cc}/{cc}.gif'.format(base_url,cc=cc.lower())
	async with aiohttp.ClientSession() as sess:
		resp=await sess.request('GET',url)
		if resp.status==200:
			image=await resp.content.read()
			return image
		elif resp.status==404:
			raise web.HTTPNotFound()
		else:
			raise aiohttp.HttpProcessingError(code=resp.status, message=resp.reason, headers=resp.headers)

async def download_one(cc, base_url, semaphore, verbose):
	#semaphore는 동시 요청 수를 제한하는 동기화 장치. asyncio.Semaphore 객체를 받는다. 
	#semaphore는 동기 카운터를 운영하다가, 최대 허용 수에 이르렀을 때만 코루틴이 블로킹된다.
	try:
		async with semaphore: 
		#Semaphore 콘텍스트 관리자는 with문에 진입할 때 (혹은 acquire() 호출 시) 카운터를 감소시키고, 빠져나갈 때 (혹은 release() 호출시) 카운터를 증가시킨다.
		#카운터가 0보다 크면 계속되고, 0이 되면 블로킹된다. 초기 카운터는 세마포어 객체를 생성할 때 생성자에 인수를 넘겨 설정한다. (예시: semaphore=asyncio.Semaphore(concur_req))
			image=await get_flag(base_url,cc)
	except web.HTTPNotFound:
		status=HTTPStatus.not_found
		msg='not found'
	except Exception as exc:
		raise FetchError(cc) from exc
	else:
		loop=asyncio.get_event_loop()
		loop.run_in_executor(None, save_flag, image, cc.lower()+'.gif') #<-run_in_executor는 스레드풀을 이용해 넘겨진 함수+인수를 돌린다.
		status=HTTPStatus.ok
		msg='OK'

	if verbose and msg:
		print(cc, msg)
	
	return Result(status,cc)

async def downloader_coro(cc_list, base_url, verbose, concur_req):
	#main에 코루틴을 직접 넘길 수 없기 때문에, 기존 download_many 내용 중 코루틴으로 실행되어야 할 부분을 떼어 중간 구조를 만들어야 했다..
	counter=collections.Counter()
	semaphore=asyncio.Semaphore(concur_req)
	to_do=[download_one(cc,base_url,semaphore,verbose) for cc in sorted(cc_list)]
	to_do_iter=asyncio.as_completed(to_do) #실행이 완료되면 Future 객체를 가져오는 반복자이다
	if not verbose:
		to_do_iter=tqdm.tqdm(to_do_iter, total=len(cc_list))
	for future in to_do_iter:
		try:
			res=await future
		except FetchError as exc:
			country_code=exc.country_code
			try:
				error_msg=exc.__cause__.args[0]
			except IndexError:
				error_msg=exc.__cause__.__class__.__name__
			if verbose and error_msg:
				msg='*** Error for {}: {}'
				print(msg.format(country_code, error_msg))
			status=HTTPStatus.error
		else:
			status=res.status #HTTPStatus.ok
		counter[status]+=1
	return counter

def download_many(cc_list, base_url, verbose, concur_req):
	#이제는 스케쥴링만 한다
	loop=asyncio.get_event_loop()
	coro=downloader_coro(cc_list, base_url, verbose, concur_req)
	counts=loop.run_until_complete(coro)
	loop.close()

	return counts

if __name__=='__main__':
	main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)