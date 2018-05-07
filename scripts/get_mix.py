import requests as r
import sys, os, json
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend') 
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend/aws') 
from s3 import S3
from dynamo import DynamoConn

from scipy.stats import linregress


datasets = [
	# 'final-homes-eigs-chicago-SA01',
	# 'final-homes-eigs-chicago-SA03',
	'final-homes-eigs-chicago-SE01',
	'final-homes-eigs-chicago-SE03',
]

# 
def keyfunction(k):
    return d[k]

for dataset in datasets:
	print dataset
	url = 'http://chicago.bnroths.com/data/%s/2015/1.json' % (dataset)
	res = r.get(url).json()

	places = {}
	for a in res['data']:
		places[a] = {'low': [], 'high': []}

	
for dataset in datasets:	
	for i in range(14):
		year = i + 2002
		url = 'http://chicago.bnroths.com/data/%s/%s/1.json' % (dataset, year)
		print url
		res = r.get(url).json()
		for neighborhood in places:
			
			try:
				num = res['data'][neighborhood]['real']
			except:
				num = 0
			if '1' in dataset:
				places[neighborhood]['low'].append(round(0.001*num, 3))
			else:
				places[neighborhood]['high'].append(round(0.001*num, 3))
	
res = {}	
for neighborhood in places:

	low = 100*linregress(range(len(places[neighborhood]['low'])), places[neighborhood]['low']).slope
	high = 100*linregress(range(len(places[neighborhood]['high'])), places[neighborhood]['high']).slope

	res[neighborhood] = low - high

for key, value in sorted(res.iteritems(), key=lambda (k,v): (v,k)):
    print "%s & %.3f \\\\" % (key, value)

