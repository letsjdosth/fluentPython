def coroutine(func):
	"""데커레이터: 'func'를 priming. 첫 번째 yield까지 진행시킨다."""
	from functools import wraps
	@wraps(func) #<-내부함수 메타데이터를 모두 외부함수로 복사
	def primer(*args,**kwargs):
		gen=func(*args,**kwargs)
		next(gen)
		return gen
	return primer