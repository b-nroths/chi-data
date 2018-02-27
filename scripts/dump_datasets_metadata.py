import sys, os, json
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend/aws') 
from s3 import S3
from dynamo import DynamoConn

d = DynamoConn()

for a in d.get_all():
	print a
	print "\n"
	print type(a)
	a['boundary'] = 'chicago'
	a.pop('boundaries', None)
	# a['table'] = json.dumps({})
	# exit(0)
	d.put_item(a)