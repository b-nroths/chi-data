import requests as r
import sys, os, json
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend') 
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend/aws') 
from s3 import S3
from dynamo import DynamoConn


datasets = [
	# 'final-jobs-eigs-chicago-S000',
	'final-jobs-eigs-chicago-SE01',
	# 'final-jobs-eigs-chicago-SE02',
	'final-jobs-eigs-chicago-SE03',
	# 'final-jobs-eigs-chicago-SI01',
	# 'final-jobs-eigs-chicago-SI02',
	# 'final-jobs-eigs-chicago-SI03',
	
]

# 
def keyfunction(k):
    return d[k]

a = []
for dataset in ['final-jobs-eigs-chicago-SI01']:
	print dataset
	url = 'http://chicago.bnroths.com/data/%s/2015/1.json' % (dataset)
	res = r.get(url).json()
	for row in sorted(res['data']):
		# print row
		a.append(res['data'][row]['real'])
print a

b = []
for dataset in ['final-jobs-eigs-chicago-SI03']:
	print dataset
	url = 'http://chicago.bnroths.com/data/%s/2015/1.json' % (dataset)
	res = r.get(url).json()
	for row in sorted(res['data']):
		# print row
		b.append(res['data'][row]['real'])

print b

def dot(A,B): 
    return (sum(a*b for a,b in zip(A,B)))

def cosine_similarity(a,b):
    return dot(a,b) / ( (dot(a,a) **.5) * (dot(b,b) ** .5) )

print cosine_similarity(a, b)