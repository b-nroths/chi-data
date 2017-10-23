# serverless deploy
# serverless invoke local --function chicago


import os, ast, sys, json, time, pprint, uuid
print sys.version

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored")) 

import requests, boto3

datasets = {
	'crimes': {
		'dataset_name': 'crimes_2001_to_present',
		'date_min': '2001-01-01',
		'columns': ['id', 'date', 'latitude', 'longitude']
	},
	'graffiti_311': {
		'dataset_name': '311_service_requests_graffiti_removal',
		'date_min': '2011-01-01',
		'columns': ['service_request_number', 'creation_date', 'latitude', 'longitude']
	},
	'vacant_311': {
		'dataset_name': '311_service_requests_vacant_and_abandoned_building',
		'date_min': '2008-01-18',
		'columns': ['service_request_number', 'date_service_request_was_received', 'latitude', 'longitude']
	},
	'alley_lights_out_311': {
		'dataset_name': '311_service_requests_alley_lights_out',
		'date_min': '2011-01-01',
		'columns': ['service_request_number', 'creation_date', 'latitude', 'longitude']
	},
	'sanitation_311': {
		'dataset_name': '311_service_requests_sanitation_code_complaints',
		'date_min': '2011-01-01',
		'columns': [None, 'creation_date', 'latitude', 'longitude']
	},
	'food_inspections': {
		'dataset_name': 'food_inspections',
		'date_min': '2010-01-04',
		'columns': ['inspection_id', 'inspection_date', 'latitude', 'longitude'],
	},
	'liquor_licenses': {
		'dataset_name': 'business_licenses_current_liquor_and_public_places',
		'date_min': '2013-05-06',
		'columns': ['license_id', 'license_term_start_date', 'latitude', 'longitude'],
	},
	'building_violations': {
		'dataset_name': 'building_violations',
		'date_min': '2006-01-01',
		'columns': ['id', 'violation_date', 'latitude', 'longitude']
	},
}

class Download():

	def __init__(self):
		self.name   = 'Ben'

	def download_data(self, dataset_name=None):
		url = 'http://plenar.io/v1/api/datadump?dataset_name=%s&data_type=json&obs_date__ge=2017-06-01' % datasets[dataset_name]['dataset_name']
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
			DeliveryStreamType='DirectPut',
			ExclusiveStartDeliveryStreamName='string'
		)
		return res['DeliveryStreamNames']
	#
	def get_stream(self, dataset):
		res = self.kinesis.describe_delivery_stream(
			DeliveryStreamName=dataset,
		)
		return res['DeliveryStreamDescription']
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
					'Prefix': 'chicago-data/%s' % dataset,
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

	def get_or_create(self, dataset):
		res = self.get(dataset)
		
	
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


k = kinesisConn()
d = dynamoConn()
def handler(event, context):
	d = Download()

	for table in datasets:
		if table not in k.list_streams():
			k.get_or_create(table)

		# res = d.download_data(table)
		# pprint.pprint(res['features'][0]['properties'])
		# exit(0)
		# new_json = d.transform_json(res['features'])
	
	return {"result": "GTG"}