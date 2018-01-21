# serverless deploy
# serverless invoke local --function datasets
import os, ast, sys, json, time, pprint, uuid, datetime, re, gzip, io, csv
from dateutil import parser

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored")) 

from aws.dynamo import DynamoConn
db = DynamoConn()

def handler(event, context):

	return {
		'statusCode': 200,
		'headers': {
			'Access-Control-Allow-Origin' : '*' # Required for CORS support to work
		},
		'body': json.dumps(db.get_datasets(), sort_keys=True)
	}

# print handler(None, None)