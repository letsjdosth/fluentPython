#딜리터
class BlackKnight:
	def __init__(self):
		self.members=['an arm','another arm','a leg','another leg']
		self.phrases=["'Tis but a scratch.","It's just a flesh wound.","I'm invincible!","All right, we'll call it a draw."]

	@property
	def member(self):
		print('next member is:')
		return self.members[0]

	@member.deleter
	def member(self):
		text='BLACK KNIGHT (loses {})\n--{}'
		print(text.format(self.members.pop(0), self.phrases.pop(0)))

knight=BlackKnight()
print(knight.member)
# next member is:
# an arm
del knight.member
# BLACK KNIGHT (loses an arm)
# --'Tis but a scratch.
del knight.member
# BLACK KNIGHT (loses another arm)
# --It's just a flesh wound.
del knight.member
# BLACK KNIGHT (loses a leg)
# --I'm invincible!
del knight.member
# BLACK KNIGHT (loses another leg)
# --All right, we'll call it a draw.


#property 대신 __setattr__,__getattr__,__detattr__로 구현해볼 수도 있음
class BlackKnight_2:
	def __init__(self):
		self.members=['an arm','another arm','a leg','another leg']
		self.phrases=["'Tis but a scratch.","It's just a flesh wound.","I'm invincible!","All right, we'll call it a draw."]
	
	@property
	def member(self):
		print('next member is:')
		return self.members[0]

	def __delattr__(self,name):
		if name=='member':
			text='BLACK KNIGHT 2 (loses {})\n--{}'
			print(text.format(self.members.pop(0), self.phrases.pop(0)))
		else:
			del self.name

knight2=BlackKnight_2()
print(knight2.member)
# next member is:
# an arm
del knight2.member
# BLACK KNIGHT 2 (loses an arm)
# --'Tis but a scratch.
del knight2.member
# BLACK KNIGHT 2 (loses another arm)
# --It's just a flesh wound.
del knight2.member
# BLACK KNIGHT 2 (loses a leg)
# --I'm invincible!
del knight2.member
# BLACK KNIGHT 2 (loses another leg)
# --All right, we'll call it a draw.