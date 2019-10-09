import unicodedata
import string
cafe='café'
order='“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'

def shave_marks(txt):
	"""발음 구별 기호 모두 제거"""
	norm_txt=unicodedata.normalize('NFD',txt) #nfd이므로 결합문자 다 분해됨
	shaved=''.join(c for c in norm_txt if not unicodedata.combining(c)) #0이면:(즉 결합문자가 아니면)
	return unicodedata.normalize('NFC',shaved)

#unicodedata.combining(chr)
#Returns the canonical combining class assigned to the character chr as integer. Returns 0 if no combining class is defined.
print(unicodedata.combining('c')) #0
print(unicodedata.combining('\u0301')) #230

print(shave_marks(cafe))
print(shave_marks(order))


def shave_marks_latin(txt):
	"""기반문자가 라틴문자인 경우에만 발음구별기호 제거"""
	norm_txt=unicodedata.normalize('NFD',txt)
	latin_base=False
	keepers=[]
	for c in norm_txt:
		if unicodedata.combining(c) and latin_base:
			continue
		
		keepers.append(c)
		if not unicodedata.combining(c):
			latin_base = (c in string.ascii_letters)  #추측: 이 검사가 뒤에있는 이유는..아마 첫 글자로 결합문자가 나오는 경우가 없어서인가 봄..
	shaved=''.join(keepers)
	return unicodedata.normalize('NFC',shaved)

print(shave_marks_latin(cafe))
print(shave_marks_latin(order))



#asciize with mapping table
single_map = str.maketrans("""‚ƒ„†ˆ‹‘’“”•–—˜›""",
                           """'f"*^<''""---~>""")
multi_map = str.maketrans({
    '€': '<euro>',
    '…': '...',
    'Œ': 'OE',
    '™': '(TM)',
    'œ': 'oe',
    '‰': '<per mille>',
    '‡': '**',
})
multi_map.update(single_map)
# print(multi_map)


def dewinize(txt):
	"""Win1252->ascii. MS가 latin1에서  win1252에 추가한 글자들을 변경"""
	return txt.translate(multi_map)
def asciize(txt):
	no_marks=shave_marks_latin(dewinize(txt))
	no_marks=no_marks.replace('ß','ss')
	return unicodedata.normalize('NFKC',no_marks)

print(dewinize(order))
print(asciize(order))