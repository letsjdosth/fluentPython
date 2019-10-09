l=[1,2,3]
print(l*5)
print(5*'abcd')

#correct
board=[['_']*3 for i in range(3)]
print(board)
board[1][2]='X'
print(board) #[['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']]


#incorrect
wierd_board=[['_']*3]*3
print(wierd_board)
wierd_board[1][2]=0
print(wierd_board) #[['_', '_', 0], ['_', '_', 0], ['_', '_', 0]]

#결론: 참조-가변 객체를 곱하거나 이런 식으로 초기화할 때 주의할 것. 초기화 시 list comp 이용 추천


l=[1,2,3]
print(id(l)) #id(): 객체의 "아이덴티티"를 돌려준다. 이것은 객체의 수명 동안 유일하고 바뀌지 않음이 보장되는 정수
l*=2
print(l,id(l)) #동일함. 복합할당 연산 +=, *=는 보통은 기존 객체를 변경함
t=(1,2,3)
print(id(t))
t*=2
print(t,id(2)) #바뀜 (tuple은 불변seq이므로, 어쩔 수 없음) #새로 만든 것이므로, 비효율적임


#+= quiz
t=(1,2,[30,40])
#t[2]+=[50,60] #error
#print(t) #idle에서 실행해보면, (1,2,[30,40,50,60])이 됨. 충격

