import asyncio

import aiohttp
from flags620 import BASE_URL, save_flag, show, main

async def get_flag(cc):
	url='{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
	async with aiohttp.ClientSession() as sess:
		resp=await sess.request('GET',url)
		image=await resp.content.read()
	return image

async def download_one(cc):
	image=await get_flag(cc)
	show(cc)
	save_flag(image, cc.lower()+'.gif')
	return cc

def download_many(cc_list):
	loop=asyncio.get_event_loop()
	to_do=[download_one(cc) for cc in sorted(cc_list)]
	wait_coro=asyncio.wait(to_do) #wait()는 일종의 코루틴으로서, Future 객체나 코루틴의 반복형을 받아 Task 안에 래핑 후 작업이 모두 완료되면 완료되는 코루틴 제너레이터를 반환한다.
	res, _=loop.run_until_complete(wait_coro)
	loop.close()

	return len(res)

if __name__=='__main__':
	main(download_many)
# VN ID FR DE JP EG CN PK NG TR BR BD IN RU ET PH US CD MX IR 
# 20 flags downloaded in 0.37s