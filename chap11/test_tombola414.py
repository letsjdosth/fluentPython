from tombola412 import Tombola

class Fake(Tombola):
	def pick(self):
		return 13
print(Fake)
Fake() #TypeError: Can't instantiate abstract class Fake with abstract methods load