import datetime
import random
import json

# base = datetime.datetime.today()
# date_list = [base - datetime.timedelta(days=x) for x in range(0, 100*365)]

# lt = {}
# for d in date_list:
# 	print str(d)[:10]
# 	lt[str(d)[:10]] = int(10000*random.random())


a = []

# with open('../frontend/public/boundaries/blocks.json') as f:
# 	text = json.loads(f.read())['features']
# 	for row in text:
# 		a.append([row['properties']['geoid10'], row['properties']['tract_bloc']])
# 	print len(text)

# with open('blocks.tsv', 'w') as f:
# 	for r in a:
# 		f.write('\t'.join(r)+'\n')
# print len(json.loads(text))

## write out census tracts
with open('../frontend/public/boundaries/tracts.json') as f:
	text = json.loads(f.read())['features']
	for row in text:
		print row['properties']['geoid10']
		a.append([row['properties']['geoid10']])
	# print len(text)

with open('../data/tracts.tsv', 'w') as f:
	for r in a:
		f.write('\t'.join(r)+'\n')
# print len(json.loads(text))