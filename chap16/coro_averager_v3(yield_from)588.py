from collections import namedtuple

Result=namedtuple('Result','count average')

#하위 제너레이터(subgenerator)
def averager():
	total=0.0
	count=0
	average=None
	while True:
		term = yield #<-자리!
		if term is None: #여기에서는 None을 중단 사인으로 선택하고 if문으로 낚아채지만, 기본 동작은 yield로 None이 전달되면 단순히 next()를 부른다.
			break
		total+=term
		count+=1
		average=total/count
	return Result(count,average) #<-리턴이 '있는' 제너레이터 함수

#대표 제너레이터(delegating generator)
def grouper(results,key):
	while True:
		results[key] = yield from averager() 
		#yield from은 받은 제너레이터를 알아서 기동시킨다(알아서 priming을 한다. 즉 첫 next()를 스스로 부른다.)
		#yield from으로 반환되는 값은 averager()의 'return값'이다. (yield값이 아님! 예에서는 애초에 값을 생성하지도 않지만.)
		
		#중간에서 대표 제너레이터가 yield from을 만나면, 작업을 해당 yield from을 통해 연결된 하위 제너레이터에 위임하고 그 작업이 끝나기를 '기다린다'. 
		#이 때, 기존의 yield를 이용하는 방식으로 호출자(main)와 하위 제너레이터(averager) 사이가 연결되어 데이터를 주고받을 수 있으며, 
		#(즉, main이 grouper를 통해 averager에 send(),throw(),closing()등을 사용 가능하며, 또한 averager의 생성값이 main으로 올라간다)
		#이후 작업이 끝나면(=하위 제너레이터인 averager가 에러로 중단되거나, 혹은 모든 줄 실행 완료 등으로 중단되면), 다시 grouper가 작동하며 yield from을 통해 예외처리된 하위 제너레이터의 리턴값을 취한다

		#하위 제너레이터의 yield는 통로를 열 위치를 지정한다
		#(yield from을 가지고 있는) grouper에 send()를 사용하면 이 값은 yield from을 통해 averager()의 yield 위치로 전달된다.(grouper에서는 해당 값을 볼 수 없다)

#호출자(caller)
def main(data):
	results={}
	for key,values in data.items():
		group=grouper(results,key) #<-루프가 돌때마다 코루틴(grouper, 또 그의 yield from을 통한 averager())을 새로 생성한다.
		next(group)
		for value in values:
			group.send(value) #<-main(호출자)에서 중간에 있는 대표 제너레이터에다 대고 직접 값을 쏜다! 이는 grouper의 yield from을 통해 averager()가 yield 위치에서 받는다!!!
		group.send(None) #<-values의 value가 다 소진되면 for문이 종료되고 다음으로 None을 쏘아 averager()를 중단시킨다. 
		#!!!중단 사인을 전달하는것이 매우 중요하다!!! (특히 하위 제너레이터가 무한루프를 이용할 경우)
		#None으로 averager를 제대로 중단시키지 않으면, 여전히 grouper는 작업을 averager에 위임한 상태로 있고 averager는 내부적으로 계속 yield에 걸려있게 되며, 
		#떄문에 grouper는 yield from을 통해 리턴값을 받을 수 없고 따라서 yield from 왼쪽의 =(대입)가 실행되지 않는다.
		#이 상태로 루프가 돌면, group 변수가 새로운 grouper객체에 바인딩되므로, 기존 grouper 제너레이터는 참조 수를 잃고 가비지 컬렉트된다.
		#(동시에 기존 grouper를 통해 참조되던 기존 averager도 가비지 컬렉트된다.)

		#때문에 None을 제대로 안 넘기면, 이 예에서는 results에 할당이 하나도 안 되고 따라서 출력이 하나도 안 나오게 된다. 
		#하지만 '에러가 안 난다'<-!!!!!!!. 조용히 넘어가게 되는것이 문제

	print(results) #for debug. 결과 dict 출력
	report(results)

#보고서 생성 함수
def report(results):
	for key, result in sorted(results.items()):
		group,unit=key.split(';')
		print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.average, unit))

data={
	'girls;kg':[40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
	'girls;m':[1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
	'boys;kg':[39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
	'boys;m':[1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46]
}

if __name__=='__main__':
	main(data)