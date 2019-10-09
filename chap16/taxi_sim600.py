import random
import collections
import queue
import argparse
import time

DEFAULT_NUMBER_OF_TAXIS=3
DEFAULT_END_TIME=180
SEARCH_DURATION=5
TRIP_DURATION=20
DEPARTURE_INTERVAL=5

Event=collections.namedtuple('Event','time proc action') #이벤트가 발생할 시각, 택시 프로세스 객체 식별자, 행동 설명 문자열

def taxi_process(ident,trips,start_time=0):
	"""하위 제너레이터
	각 상태 변화마다 이벤트를 발생시키고 이후 시뮬레이터에 제어권을 넘긴다. (코루틴을 이용한 동시성에서는 중앙 스케줄러에 제어권을 넘길 타이밍을 하위 제너레이터가 자발적으로 정한다.(스레드 이용시는 반대임))
	택시마다 한번씩 호출되어 택시 행동을 나타내는 제너레이터
	ident: 택시 번호, trips:집에 돌아가기 전 택시가 수행할 운행 횟수, start_time:택시가 차고를 나오는 시각
	"""
	time=yield Event(start_time, ident,'leave garage') #시뮬 루프에 이벤트를 보내고 대기. 시뮬 루프에서 이 제너레이터를 재호출시 시간을 보내옴
	for i in range(trips):
		time=yield Event(time, ident, 'pick up passenger')
		time=yield Event(time, ident, 'drop off passenger')
	yield Event(time, ident, 'going home')
	#마지막 줄에 도달 시 StopIteration 예외 발생


class Simulator:
	def __init__(self, procs_map):
		self.events=queue.PriorityQueue() #PriorityQueue는 항목을 넣으면 알아서 정렬하고 순서대로 꺼내온다. #Event는 첫 요소인 time을 가지고 정렬된다
		self.procs=dict(procs_map) #i:generator of i 가 들어있는 dict의 사본을 저장한다.

	def run(self, end_time):
		"""시간이 만료될 때까지 이벤트를 스케줄링하고 출력"""
		#각 택시마다 첫 이벤트를 스케줄링
		for _, proc in sorted(self.procs.items()): #모든 제너레이터를 기동시키고 events 큐에 항목을 넣는다
			first_event=next(proc)
			self.events.put(first_event) #put: 큐에 항목을 넣는다 / get: 큐에서 항목을 가져온다
		
		#시뮬레이션 메인 루프
		sim_time=0
		while sim_time<end_time:
			if self.events.empty():
				print('*** end of events ***')
				break
			
			#time에 따라 Event 고르고 출력
			current_event=self.events.get() #PriorityQueue에서 get하므로, (자동)정렬 기준인 가장 작은 time값을 가진 Event를 가져온다
			sim_time, proc_id, previous_action=current_event #언패킹 및 sim_time 갱신 #previous action은 51줄까지는 이번 액션이다! (54줄의 compute_duration부터는 이전 액션이고 거기서 써먹기 때문에 이름이 이러함)
			print('taxi:',proc_id, proc_id*'   ' ,current_event)
			active_proc=self.procs[proc_id]
			
			#해당 택시 제너레이터를 동작시켜 다음 Event 생성 후 events 큐에 등록
			next_time=sim_time+compute_duration(previous_action)
			try:
				next_event=active_proc.send(next_time)
			except StopIteration:
				del self.procs[proc_id]
			else:
				self.events.put(next_event)
		else: #while 루프에서 sim_time<end_time이 False가 되었을 경우 진입 (break시에는 진입하지 않는다)
			msg='***end of simulation time: {} event pending ***'
			print(msg.format(self.events.qsize()))


def compute_duration(previous_action):
	"""지수분포를 이용해 행동 기간을 계산"""
	if previous_action in ['leave garage', 'drop off passenger']:
		#손님 없이 배회
		interval=SEARCH_DURATION
	elif previous_action=='pick up passenger':
		#손님을 태우고 운행
		interval=TRIP_DURATION
	elif previous_action=='going home':
		interval=1
	else:
		raise ValueError('Unknown previous_action: %s' % previous_action)
	return int(random.expovariate(1/interval))+1


def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,seed=None):
	"""난수생성기 초기화, 프로세스 생성, 시뮬레이션 실행"""
	if seed is not None:
		random.seed(seed)

	taxis={i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL) for i in range(num_taxis)} #<- i: generator of i 가 택시 대수만큼 들어간다
	sim=Simulator(taxis)
	sim.run(end_time)

if __name__=='__main__':
	parser=argparse.ArgumentParser(description='Taxi fleet simulator.')
	parser.add_argument('-e','--end-time',type=int,default=DEFAULT_END_TIME,help='simulation end time; default = %s' % DEFAULT_END_TIME)
	parser.add_argument('-t','--taxis',type=int,default=DEFAULT_NUMBER_OF_TAXIS,help='number of taxis running; default = %s' % DEFAULT_NUMBER_OF_TAXIS)
	parser.add_argument('-s','--seed',type=int,default=None,help='random generator seed (for testing)')
	args=parser.parse_args()
	main(args.end_time, args.taxis, args.seed)

