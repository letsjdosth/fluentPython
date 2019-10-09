import os
import time
import sys

import requests

POP20_CC='CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
BASE_URL='http://flupy.org/data/flags'

DEST_DIR='C:/newpyscript/fluentPython/chap17/downloads'

def save_flag(img, filename):
	path=os.path.join(DEST_DIR, filename)
	with open(path, 'wb') as fp:
		fp.write(img)

def get_flag(cc):
	url='{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
	resp=requests.get(url)
	return resp.content

def show(text):
	print(text, end=' ')
	sys.stdout.flush() 
	#표준 출력(sys.stdout. 디스크 쓰기 등) 시, 일반적으로는 버퍼(데이터 이동 등을 위한 임시 저장공간)에 데이터를 저장하고 있다가 버퍼가 다 차면 한꺼번에 출력함. 
	#flush()는 버퍼 데이터 전체를 곧바로 모두 출력하고 버퍼를 비우도록 함.

def download_many(cc_list):
	for cc in sorted(cc_list):
		image=get_flag(cc)
		show(cc)
		save_flag(image, cc.lower()+'.gif')
	return len(cc_list)

def main(download_many):
	t0=time.time()
	count=download_many(POP20_CC)
	elapsed=time.time()-t0
	msg='\n{} flags downloaded in {:.2f}s'
	print(msg.format(count, elapsed))

if __name__=='__main__':
	main(download_many)

# BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN 
# 20 flags downloaded in 6.59s
# [Finished in 6.8s]