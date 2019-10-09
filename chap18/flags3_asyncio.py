#메타데이터를 이용해서, 국기 파일 다운로드 시 파일명을 국가코드 뿐 아니라 국가 이름도 같이 쓰도록 하자.
#metadata.json format	
#{"tld_cc": ".ad", "iso_cc": "AD", "country": "Andorra", "gec_cc": "AN"}

import asyncio
import collections
import aiohttp
from aiohttp import web
import tqdm

from flags2_asyncio import DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ, FetchError
from flags2_common import main, HTTPStatus, Result, save_flag

async def http_get(url):
	async with aiohttp.ClientSession() as sess:
		res=await sess.request('GET',url)
	if res.status==200:
		ctype=res.headers.get('Content-type','').lower()
		if 'json' in ctype or url.endswith('json'): #get 결과가 json파일이면
			data=await res.json() #dict로 데이터를 받는다
		else: #get 결과가 json이 아니면(->gif이면)
			data=await res.read() #그대로 읽는다
		return data
	elif res.status==404:
		raise web.HTTPNotFound()
	else:
		raise aiohttp.errors.HttpProcessingError(code=res.status, message=res.reason, headers=res.headers)

async def get_country(base_url,cc):
	url='{}/{cc}/metadata.json'.format(base_url,cc=cc.lower())
	metadata=await http_get(url)
	return metadata['country']

async def get_flag(base_url,cc):
	url='{}/{cc}/{cc}.gif'.format(base_url,cc=cc.lower())
	return await http_get(url)

async def download_one(cc, base_url, semaphore, verbose):
	try:
		async with semaphore:
			image=await get_flag(base_url,cc)
		async with semaphore:
			country=await get_country(base_url,cc)
	except web.HTTPNotFound:
		status=HTTPStatus.not_found
		msg='not found'
	except Exception as exc:
		raise FetchError(cc) from exc
	else:
		country=country.replace(' ','_')
		filename='{}-{}.gif'.format(country,cc)
		loop=asyncio.get_event_loop()
		loop.run_in_executor(None, save_flag, image, filename)
		status=HTTPStatus.ok
		msg='OK'
	if verbose and msg:
		print(cc,msg)
	return Result(status,cc)

async def downloader_coro(cc_list, base_url, verbose, concur_req):
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
	loop=asyncio.get_event_loop()
	coro=downloader_coro(cc_list, base_url, verbose, concur_req)
	counts=loop.run_until_complete(coro)
	loop.close()

	return counts


if __name__=='__main__':
	main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)