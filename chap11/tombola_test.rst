==============
Tombola 테스트
==============

반복형에서 객체를 생성해 로딩::

>>> balls=list(range(3))
>>> globe=ConcreteTombola(balls)
>>> globe.loaded()
True
>>> globe.inspect()
(0, 1, 2)

수집::

>>> picks=[]
>>> picks.append(globe.pick())
>>> picks.append(globe.pick())
>>> picks.append(globe.pick())

결과 확인::

>>> globe.loaded()
False
>>> sorted(picks)==balls
True

재로딩::

>>> globe.load(balls)
>>> globe.loaded()
True
>>> picks=[globe.pick() for i in balls]
>>> globe.loaded()
False

비어있을 때 LookupError 예외 발생 확인::

>>> globe=ConcreteTombola([])
>>> try:
...    globe.pick()
... except LookupError as exc:
...    print('OK')
OK

100개 로딩 후 꺼내기::

>>> balls=list(range(100))
>>> globe=ConcreteTombola(balls)
>>> picks=[]
>>> while globe.inspect():
...    picks.append(globe.pick())
>>> len(picks)==len(balls)
True
>>> set(picks)==set(balls)
True

순서 변경 확인::

>>> picks != balls
True
>>> picks[::-1] != balls
True