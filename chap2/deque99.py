from collections import deque

dq=deque(range(10),maxlen=10) #최대길이 10 (선택 요소임)
print(dq)

dq.rotate(3) #3번 오른쪽으로 민다
print(dq)

dq.rotate(-4) #4번 왼쪽으로 민다
print(dq)

dq.appendleft(-1) #왼쪽에 -1 추가 (maxlen을 맞추기 위해 밀리며 맨 오른쪽 하나가 삭제된다)
print(dq)

dq.extend([11,12,13]) #오른쪽에 [11,12,13] 추가 (밀리며 왼쪽 3개가 삭제된다)
print(dq)

dq.extendleft([10,20,30,40]) #왼쪽에 추가. iter를 이용하여 하나씩 추가하므로, 역순으로 들어간다
print(dq) #deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)