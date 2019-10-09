import time
import functools

DEFAULT_FMT='[{elapsed:0.8f}s] {name}({arg_str}) -> {_result}'

def clock3(fmt=DEFAULT_FMT):
	def decorate(func):
		@functools.wraps(func)
		def clocked(*_args,**_kwargs):
			t0=time.perf_counter()
			_result=func(*_args,**_kwargs)
			elapsed=time.perf_counter()-t0
			name=func.__name__
			arg_lst=[]
			if _args:
				arg_lst.append(', '.join(repr(arg) for arg in _args))
			if _kwargs:
				pairs=['%s=%r'%(k,w) for k,w in sorted(_kwargs.items())]
				arg_lst.append(', '.join(pairs))
			arg_str=', '.join(arg_lst)
			# print('[%0.8fs] %s(%s) -> %r'%(elapsed,name,arg_str,result))
			# print(locals())
			print(fmt.format(**locals()))
			return _result
		return clocked
	return decorate


@clock3()
def snooze(seconds):
	time.sleep(seconds)

@clock3('{name}: {elapsed}s')
def snooze2(seconds):
	time.sleep(seconds)

@clock3('{name}({arg_str}) dt={elapsed:0.3f}s')
def snooze3(seconds):
	time.sleep(seconds)

for i in range(3):
	snooze(seconds=.123)


for i in range(3):
	snooze2(.123)

for i in range(3):
	snooze3(.123)