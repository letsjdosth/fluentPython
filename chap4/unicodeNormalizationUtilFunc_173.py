"""
>>> s1='café'
>>> s2='cafe\u0301'
>>> s1,s2
('café', 'café')
>>> s1==s2
False
>>> nfc_equal(s1,s2)
True
>>> fold_equal(s1,s2)
True
>>> s3='Straße'
>>> s4='strasse'
>>> s3==s4
False
>>> nfc_equal(s3,s4)
False
>>> fold_equal(s3,s4)
True
>>> nfc_equal('A','a')
False
>>> fold_equal('A','a')
True
"""


from unicodedata import normalize

def nfc_equal(str1,str2):
	return normalize('NFC',str1)==normalize('NFC',str2)

def fold_equal(str1,str2):
	return normalize('NFC',str1).casefold()==normalize('NFC',str2).casefold()


if __name__ == "__main__":
    import doctest
    doctest.testmod()