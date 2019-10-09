#목표: osconfeed에서, speaker,conference,venue의 일련번호를 키로 사용해 접근하기 편하도록 구조를 바꾸자.

import shelve #https://docs.python.org/ko/3/library/shelve.html?highlight=shelve#module-shelve
import warnings

import osconfeed707

DB_NAME='data/schedule1_db'
CONFERENCE='conference.115' #존재한다고 알려져 있는 키 대표

class Record:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs) #<-kwargs로 매핑형이 들어올 때 자주 쓰는 꼼수. 매핑형대로 바로 속성 묶음을 빠르게 정의할 수 있다

def load_db(db):
	"""점표기법을 사용할 수 있도록 변환 (쉘브 db에 키로, 점표기된 모든 경우의 수를 집어넣는 방식임)"""
	raw_data=osconfeed707.load()
	warnings.warn('loading '+DB_NAME)
	for collection, rec_list in raw_data['Schedule'].items():
		record_type=collection[:-1] #마지막 s를 제거한다. events->event 등
		for record in rec_list:
			key='{}.{}'.format(record_type, record['serial']) #event.34505 같은 식으로 키를 설정한다
			record['serial']=key #serial 필드 재설정
			db[key]=Record(**record)

#for test
if __name__=='__main__':
	db=shelve.open(DB_NAME)
	if CONFERENCE not in db:
		load_db(db)
	speaker=db['speaker.3471']
	print(type(speaker))
	print(speaker.name, speaker.twitter)
	db.close()