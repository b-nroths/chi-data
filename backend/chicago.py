# serverless deploy
# serverless invoke local --function chicago
import os, ast, sys, json, time, pprint, uuid, datetime
from dateutil import parser

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored")) 

import requests, boto3
from boto3.dynamodb.conditions import Key


import pandas as pd
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from dynamo import dynamoConn

class Download():

	def __init__(self):
		self.name   = 'Ben'

	def download_data(self, dataset_long_name, dt):
		print dt
		year, month = dt.split('-')
		next_month = (datetime.date(int(year), int(month), 1) + datetime.timedelta(days=32)).strftime('%Y-%m')
		# dt_plus_one = (parser.parse(dt) + datetime.timedelta(month=1)).strftime('%Y-%m-%d')
		# print dt_plus_one
		url = 'http://plenar.io/v1/api/datadump?dataset_name=%s&data_type=json&obs_date__ge=%s-01&obs_date__le=%s-01' % (dataset_long_name, dt, next_month)
		print url
		response = requests.get(url).text
		datas = []
		for i, row in enumerate(json.loads(response.replace("'type': 'FeatureCollection', 'features':", '"type": "FeatureCollection", "features":').replace('},]', '}]'))['features']):
			# print row
			if 'crimes' in dataset_long_name:
				if dt in row['properties']['date']:
					datas.append(row['properties'])
			else:
				if dt in row['properties']['point_date']:
					datas.append(row['properties'])
		response = pd.DataFrame(datas)
		table = pa.Table.from_pandas(response)
		# print table
		return table, len(response)

	def transform_json(self, json):
		arr = []
		for row in json:
			arr.append(row['properties'])
		return arr





class S3():
	def __init__(self):
		self.s3 	= boto3.client('s3')
		
	def list_files(self, dataset):
		get_files = True
		marker = None
		while get_files:

			res = self.s3.list_objects(
				Bucket='bnroths',
				Prefix='chicago-data/%s' % dataset,
				Marker=marker
			)
			fnames = []
			for file in res['Contents']:
				folder, dataset, year, month, day, minutes, fname = file['Key'].split('/')
				fnames.append('%s-%s-%s' % (year.replace('year=',''), month.replace('month=', day)))

			print res['Marker']
			if res['Marker']:
				marker = res['Marker']
			else:
				get_files = False

			exit(0)
			return fnames

	def save_file(self, filename, dataset_name, year):
		self.s3.upload_file(filename, 
			'bnroths', 
			'chicago-data/%s/year=%s/%s.parquet' % (dataset_name, year, filename))
		return True

	def rec_s3_dynamo(self, dataset):
		'''
		Some datasets were deleted from s3 but are still in dynamoDB cnt
		'''
		pass

db = dynamoConn()
d  = Download()
s3 = S3()

def handler(event, context):

	for dataset_item in db.get_all(data_source='plenario'):
		dataset_name = dataset_item['dataset']
		# print dataset_name
		if 'cnts' not in dataset_item:
			cnts = {}
		else:
			cnts = json.loads(dataset_item['cnts'])
		days = set(cnts.keys())
		
		## add metadata to dynamo if new
		if not db.get(dataset_name):
			db.put_item(dataset_item)
		
		## get all possible year/month combos
		min_dt     = parser.parse(dataset_item['dataset_start']).date()
		today      = datetime.datetime.today().date()
		num_days   = (today - min_dt).days
		date_list  = sorted(list(set([(today - datetime.timedelta(days=x)).strftime('%Y-%m') for x in range(num_days)])))
		# print len(date_list)
		# print len(days)
		# exit(0)
		## download data
		# print 'h', sorted((set(date_list) - days))
		# exit(0)
		for dt in sorted((set(date_list) - days)):
			year, month = dt.split('-')
			# print 'hi', dt
			# exit(0)
			table, cnt = d.download_data(dataset_long_name=dataset_item['dataset_long_name'], dt=dt)
			
			## save to s3
			# write local
			filename = '%s-%s-%s.parquet' % (dataset_name, year, month)
			pq.write_table(table, filename)
			s3.save_file(filename, dataset_name, year, month)
			os.remove(filename)
			# save cnt
			cnts[dt] = cnt
			dataset_item['cnts'] = json.dumps(cnts)
			db.put_item(dataset_item)
			
		## add example datapoint if not there
		if 'example_data' not in dataset_item:
			dataset_item['example_data'] = json.dumps(res['features'][-1])
			db.put_item(dataset_item)

	
	return {"result": "GTG"}

handler(None, None)