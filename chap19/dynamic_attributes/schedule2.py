import shelve
import warnings
import inspect

import osconfeed707

DB_NAME='data/schedule2_db'
CONFERENCE='conference.115'

class Record:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	def __eq__(self,other):
		if isinstance(other, Record):
			return self.__dict__==other.__dict__
		else:
			return NotImplemented

class MissingDatabaseError(RuntimeError):
	"""필요한 데이터베이스가 설정되어 있지 않을 때 발생시킨다"""

class DBRecord(Record):
	__db=None #staticmethod로 이 변수에 접근할것이기 때문에, 인스턴스가 아닌 클래스 변수로 만든다

	@staticmethod
	def set_db(db):
		DBRecord.__db=db #받은 db에 대한 참조 보관

	@staticmethod
	def get_db():
		return DBRecord.__db

	@classmethod
	def fetch(cls, ident):
		"""데이터를 가져온다"""
		db=cls.get_db()
		try:
			return db[ident]
		except TypeError:
			if db is None:
				msg="database not set; call '{}.set_db(my_db)"
				raise MissingDatabaseError(msg.format(cls.__name__))
			else:
				raise

	def __repr__(self):
		if hasattr(self, 'serial'):
			cls_name=self.__class__.__name__ 
			#여기 및 이 밑에서 __class__를 붙여주는 이유는, 현재 다루는 데이터가 점표기법을 사용하기 때문에, 혼선 방지를 위함이다 (잘못해서 해당 이름 레코드가 있으면 꼬인다)
			return '<{} serial={!r}>'.format(cls_name, self.serial)
		else:
			return super().__repr__()

class Event(DBRecord):
	@property
	def venue(self):
		key='venue.{}'.format(self.venue_serial)
		return self.__class__.fetch(key)
	
	@property
	def speakers(self):
		if not hasattr(self, '_speaker_objs'):
			spkr_serials=self.__dict__['speakers']
			fetch=self.__class__.fetch
			self._speaker_objs=[fetch('speaker.{}'.format(key)) for key in spkr_serials]
		return self._speaker_objs

	def __repr__(self):
		if hasattr(self,'name'):
			cls_name=self.__class__.__name__
			return '<{} {!r}>'.format(cls_name, self.name)
		else:
			return super().__repr__()

def load_db(db):
	"""점표기법을 사용할 수 있도록 변환(사실 점표기된 모든 경우를 다 dict의 키로 집어넣는 것임).
	 단, 해당 레코드타입과 맞는 클래스 정의가 전역에 있으면 해당 클래스를 가져다 쓴다"""
	raw_data=osconfeed707.load()
	warnings.warn('loading '+DB_NAME)
	for collection, rec_list in raw_data['Schedule'].items():
		record_type=collection[:-1] #conference, event, speaker, venue 중 하나가 된다
		cls_name=record_type.capitalize() 
		cls=globals().get(cls_name, DBRecord) 
		#전역범위에서 해당 타입과 같은 이름의 클래스의 객체를 가져온다. 없으면 DbRecord를 가져온다
		#(위에 Event가 있다! 따라서 event 데이터는 Event 클래스를 이용하게 될 것이다. Speaker 클래스 등도 필요하다면 만들어볼 수 있다) 
		#단, 이 코드를 염두하지 않고 어쩌다 다른 용도의  Speaker, Venue 같은 이름을 가진 클래스를 만들어버리면 꼬이는 원인이 되니, 주의할 것
		if inspect.isclass(cls) and issubclass(cls, DBRecord):
			factory=cls
		else:
			factory=DBRecord
		for record in rec_list:
			key='{}.{}'.format(record_type, record['serial'])
			record['serial']=key
			db[key]=factory(**record)


#for test
if __name__=='__main__':
	with shelve.open(DB_NAME) as db:
		if CONFERENCE not in db:
			db=load_db(db)
		DBRecord.set_db(db)
		event=DBRecord.fetch('event.33950') #<-event이므로 Event 클래스를 이용해 만들어졌을 것이다.
		print(repr(event)) #<Event 'There *Will* Be Bugs'> #<-클래스 네임 자리에 기대대로 Event가 찍혔다
		print(repr(event.venue)) #<DBRecord serial='venue.1449'> #<-Event 클래스의 property를 이용한다. 
		#@property에서 fetch를 부르고 얘는 get_db()를 통해 __db에서 레코드를 꺼내오므로, venue는 DBRecord 객체로 반환되고 그 밑의 데이터들을 다 가지고 있게 된다.
		#또한 해당 객체의 repr 형식으로 출력된다.
		print(repr(event.venue.name)) #'Portland 251' #밑의 데이터를 다 가진 DBRecord 객체이기 때문에 이렇게 참조소환(de-reference, 포인터가 가리키는 곳의 값을 가져오는 것)이 가능해진다
		for spkr in event.speakers:
			print('{0.serial}: {0.name}'.format(spkr))
		# speaker.3471: Anna Martelli Ravenscroft
		# speaker.5199: Alex Martelli
