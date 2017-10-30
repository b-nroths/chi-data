# serverless deploy
# serverless invoke local --function chicago


import os, ast, sys, json, time, pprint, uuid
print sys.version

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored")) 

import requests, boto3
from boto3.dynamodb.conditions import Key
from dateutil import parser
from datetime import datetime, timedelta
class Download():

	def __init__(self):
		self.name   = 'Ben'

	def download_data(self, dataset_long_name, date_max):
		
		print date_max
		if ((datetime.now() - date_max).days) > 60:
			dt1 = date_max.strftime('%Y-%m-%d')
			dt2 = (date_max + timedelta(days=60)).strftime('%Y-%m-%d')
			print(dt1, dt2)
			url = 'http://plenar.io/v1/api/datadump?dataset_name=%s&data_type=json&obs_date__ge=%s&obs_date__le=%s' % (dataset_long_name, dt1, dt2)
		else:
			url = 'http://plenar.io/v1/api/datadump?dataset_name=%s&data_type=json&obs_date__ge=%s' % (dataset_long_name, dt1)
		print url	
		response = requests.get(url).text
		# BUG need to replace quotes
		response = response.replace("'type': 'FeatureCollection', 'features':", '"type": "FeatureCollection", "features":')
		return json.loads(response)

	def transform_json(self, json):
		arr = []
		for row in json:
			arr.append(row['properties'])
		return arr

class kinesisConn():
	def __init__(self):
		self.kinesis = boto3.client('firehose')
	#
	def list_streams(self):
		res = self.kinesis.list_delivery_streams(
			Limit=100,
		)
		return res['DeliveryStreamNames']
	#
	def get_stream(self, dataset):
		res = self.kinesis.describe_delivery_stream(
			DeliveryStreamName=dataset,
		)
		return res['DeliveryStreamDescription']
	#
	def put_records(self, stream, records):
		res = self.kinesis.put_record_batch(
			DeliveryStreamName=stream,
			Records=records
		)
		return True
	#
	def delete_stream(self, dataset):
		res = self.kinesis.delete_delivery_stream(
			DeliveryStreamName=dataset
	)
	#
	def get_or_create(self, dataset):
		if dataset in self.list_streams():
			return True
		else:
			response = self.kinesis.create_delivery_stream(
				DeliveryStreamName=dataset,
				DeliveryStreamType='DirectPut',
				S3DestinationConfiguration={
					'RoleARN': 'arn:aws:iam::617449064033:role/firehose_delivery_role',
					'BucketARN': 'arn:aws:s3:::bnroths',
					'Prefix': 'chicago-data/%s/' % dataset,
					'BufferingHints': {'SizeInMBs': 50, 'IntervalInSeconds': 60 },
					'CompressionFormat': 'UNCOMPRESSED',
					'EncryptionConfiguration': {'NoEncryptionConfig': 'NoEncryption',},
					'CloudWatchLoggingOptions': {'Enabled': True, 'LogGroupName': '/aws/kinesisfirehose/%s' % dataset, 'LogStreamName': 'S3Delivery'}
				}
			)

class dynamoConn():
	def __init__(self):
		self.dynamodb 	= boto3.resource('dynamodb')
		self.table 		= self.dynamodb.Table('chicago-data')

	def put_item(self, json_data):
		res = self.table.put_item(Item=json_data)
		
	def get_all(self, data_source=None):
		if data_source:
			response = self.table.scan(
				FilterExpression=Key('data_source').eq('plenario')
			)
		else:
			response = table.scan()

		return response['Items']

	def get(self, dataset):
		response = self.table.get_item(
		   Key={
				'dataset': dataset
			}
		)
		if 'Item' in response:
			return response['Item']
		else:
			return None


k  = kinesisConn()
db = dynamoConn()
d  = Download()

def handler(event, context):

	for dataset_item in db.get_all(data_source='plenario'):
		dataset = dataset_item['dataset']
		print 'a'
		## add metadata to dynamo if new
		if not db.get(dataset):
			db.put_item(dataset_item)
		print 'b'
		## make streams id not exists
		if dataset not in k.list_streams():
			k.get_or_create(dataset)
		print 'c'
		## download data
		# keep track of max date for data we see
		date_max = date_max = parser.parse(dataset_item['dataset_start'])
		if 'date_max' in dataset_item:
			date_max = dataset_item['date_max']
		res = d.download_data(dataset_long_name=dataset_item['dataset_long_name'], date_max=date_max)
		
		batch = []
		for i, row in enumerate(res['features']):
			## do anything to transform data

			## update date
			# print i
			dt = parser.parse(row['properties']['date'])
			if dt >= date_max or not date_max:
				date_max = dt

			kinesisRecord = {'Data': b'%s\n' % json.dumps(row)}
			batch.append(kinesisRecord)
			if i % 100 == 0:
				k.put_records(stream=dataset, records=batch)
				batch = []
		k.put_records(stream=dataset, records=batch)

		## add example datapoint if not there
		if 'example_data' not in dataset:
			dataset_item['example_data'] = json.dumps(res['features'][-1])
			db.put_item(dataset_item)

		print date_max
		if date_max:
			dataset_item.pop('date_min', None)
			dataset_item['date_max'] = date_max
			db.put_item(dataset_item)
		exit(0)
	
	return {"result": "GTG"}