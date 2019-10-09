# import locale

fruits=['caju','atemoia','cajá','açaí','acerola']
print(sorted(fruits))
#올바른 리턴: ['açaí','acerola','atemoia','cajá','caju']
#실제 리턴: ['acerola', 'atemoia', 'açaí', 'caju', 'cajá']


#locale.strxfrm()으로 변환해 정렬
#strxfrm():현지어 비교에 사용할 수 있는 문자열로 반환

# locale.setlocale(locale.LC_COLLATE,'pt_BR.UTF-8')
# sorted_fruits=sorted(fruits,key=locale.strxfrm)
# print(sorted_fruits)
#위 코드가 뭔가 문제가있나봄(윈도에서는 안도나봄)


fruits2=['사과','복숭아','포도','배']
print(sorted(fruits2))


#using pyUca (unicode collation algorithm; 유니코드 대조 알고리즘)
import pyuca
coll=pyuca.Collator()
fruits=['caju','atemoia','cajá','açaí','acerola']
sorted_fruits=sorted(fruits,key=coll.sort_key)
print(sorted_fruits)