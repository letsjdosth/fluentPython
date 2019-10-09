#Future 객체 구경용

from concurrent import futures

from flags620 import save_flag, get_flag, show, main

MAX_WORKERS=20

def download_one(cc):
	image=get_flag(cc)
	show(cc)
	save_flag(image, cc.lower()+'.gif')
	return cc

def download_many(cc_list):
	cc_list=cc_list[:5]
	with futures.ThreadPoolExecutor(max_workers=3) as executor:
		to_do=[]
		for cc in sorted(cc_list): #<-알파벳순 반복
			future=executor.submit(download_one, cc) #<-executor 스케줄에 등록한다. 해당 작업에 해당하는 Future 객체가 반환된다.
			to_do.append(future)
			msg='Scheduled for {}: {}'
			print(msg.format(cc, future))
		
		results=[]
		for future in futures.as_completed(to_do): #<-as_completed는 Future가 완료될 때 해당 Future 객체를 생성한다.
			res=future.result() #<-Future 객체에서 결과를 가져온다.
			msg='{} result: {!r}'
			print(msg.format(future, res))
			results.append(res)
	return len(results)

if __name__=='__main__':
	main(download_many)

# Scheduled for BR: <Future at 0x40df170 state=running> #<-state에 Future 객체의 상태가 보인다. max_workers를 3으로 설정했기 때문에, 3개만 먼저 돈다.
# Scheduled for CN: <Future at 0x40df5d0 state=running>
# Scheduled for ID: <Future at 0x40df9b0 state=running>
# Scheduled for IN: <Future at 0x40dfd30 state=pending> #<-대기. 작업자 스레드를 기다린다.
# Scheduled for US: <Future at 0x40dfd90 state=pending>
# BR CN <Future at 0x40df170 state=finished returned str> result: 'BR' #<-맨 앞에 BR CN은 download_one이 출력한 메시지이다.(show 함수) 그 뒤는 Future 객체의 repr 출력이다.
# <Future at 0x40df5d0 state=finished returned str> result: 'CN' #<-앞 3개는 동시에 돌고있으므로, download_one의 show가 Future 출력과 섞일 경우가 생긴다
# ID <Future at 0x40df9b0 state=finished returned str> result: 'ID'
# IN <Future at 0x40dfd30 state=finished returned str> result: 'IN'
# US <Future at 0x40dfd90 state=finished returned str> result: 'US'

# 5 flags downloaded in 0.70s
# [Finished in 0.9s]