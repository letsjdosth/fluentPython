from urllib.request import urlopen
import warnings
import os
import json

URL='http://www.oreilly.com/pub/sc/osconfeed'
JSON='data/osconfeed.json'

def load():
	if not os.path.exists(JSON):
		msg='downloading {} to {}'.format(URL, JSON)
		warnings.warn(msg)
		with urlopen(URL) as remote, open(JSON, 'wb', encoding='utf8') as local:
			local.write(remote.read())
	with open(JSON, encoding='utf8') as fp:
		return json.load(fp)

#for test
if __name__=='__main__':
	feed=load()
	for key,value in sorted(feed['Schedule'].items()):
		print('{:3} {}'.format(len(value), key))
	# 1 conferences
	# 494 events
	# 357 speakers
  	# 53 venues
	print(feed['Schedule']['speakers'][-1]['name']) #Carina C. Zona
