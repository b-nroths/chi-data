# serverless deploy
# serverless invoke local --function chicago


## TO ADD NEW DATA NEED DATASET NAME START DATE EXAMPLE DATAPOINT IN DYNAMODB
import os, ast, sys, json, time, pprint, uuid, datetime, s3fs, json
from dateutil import parser

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored")) 

import requests, boto3, pickle
from boto3.dynamodb.conditions import Key
from json2parquet import load_json, ingest_data, write_parquet

import pandas as pd
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from aws.dynamo import DynamoConn
from aws.s3 import S3


class Download():

	def __init__(self):
		self.name   = 'Ben'

	def download_data(self, dataset_long_name, dt, schema):
		print dt
		# print schema
		year, month = dt.split('-')
		next_month = (datetime.date(int(year), int(month), 1) + datetime.timedelta(days=32)).strftime('%Y-%m')
		
		url = 'http://plenar.io/v1/api/datadump?dataset_name=%s&data_type=json&obs_date__ge=%s-01&obs_date__le=%s-01' % (dataset_long_name, dt, next_month)
		# print url
		response = requests.get(url).text
		datas = []
		for i, row in enumerate(json.loads(response.replace("'type': 'FeatureCollection', 'features':", '"type": "FeatureCollection", "features":').replace('},]', '}]'))['features']):
			# only add row if it is in the month

			if 'crimes' in dataset_long_name:
				if dt in row['properties']['date']:
					datas.append(row['properties'])
			else:
				if dt in row['properties']['point_date']:
					datas.append(row['properties'])
			# print i, row

		if datas:
			table = ingest_data(datas, schema)
			# print "HI", datas
			filename = '%s.parquet' % (month)
			write_parquet(table, filename)
		
			return filename, len(datas)
		else:
			return False, False

	def transform_json(self, json):
		arr = []
		for row in json:
			arr.append(row['properties'])
		return arr

##
## this method gets data year-montho combos and then downloads data and updates counts
##
def handler(event, context):
	
	for dataset_item in db.get_all(data_source='Plenario'):
		dataset_name = dataset_item['dataset']
		print dataset_name
		if 'cnts' not in dataset_item:
			cnts = {}
		else:
			cnts = json.loads(dataset_item['cnts'])

		days = set([str(x) for x in cnts.keys()])
		
		## get all possible year/month combos
		min_dt     = parser.parse(dataset_item['dataset_start']).date()
		today      = datetime.datetime.today().date()
		num_days   = (today - min_dt).days
		date_list  = sorted(list(set([(today - datetime.timedelta(days=x)).strftime('%Y-%m') for x in range(num_days)])))
		
		## use example data to get schema
		example_data = [json.loads(dataset_item['example_data'])['properties']]
		schema = ingest_data(example_data).schema
		
		days_to_run = set(date_list) - days 
		## rerun last two timeframes
		days_to_run.add(date_list[-1])
		days_to_run.add(date_list[-2])
		# print sorted(days_to_run)
		for dt in sorted(days_to_run):
			year, month = dt.split('-')
			table, cnt = d.download_data(
				dataset_long_name=dataset_item['dataset_long_name'], 
				dt=dt,
				schema=schema)
			# print "HI", dt
			if table:
				# print "bye"
				# print table
				filename = '%s.parquet' % (month)
				print dt, filename, dataset_name, year, cnt
				
				s3.save_file(
					filename, 
					dataset_name, 
					year,
					month)
				os.remove(filename)
				
				cnts[dt] = cnt
				dataset_item['cnts'] = json.dumps(cnts)
				dataset_item['last_updated'] = str(datetime.datetime.now())
				db.put_item(dataset_item)
			# exit(0)
	return {"result": "GTG"}

##
## this method formts the data and uploads it to the public endpoints for the web
## run_all runs over all timestamps
##
def save_data(run_all=False):
	S3FS = s3fs.S3FileSystem()

	s3 = S3()
	db = DynamoConn()

	dates = {}
	datasets = db.get_datasets()
	for dataset in datasets:
		# print dataset
		if datasets[dataset]['source'] == 'Plenario':
			
			today      = datetime.datetime.today().date()
			date_list  = set([today.strftime('%Y-%m')]) 
			date_list.add((today-datetime.timedelta(days=32)).strftime('%Y-%m'))
			date_list  = sorted(list(set([(today - datetime.timedelta(days=x)).strftime('%Y-%m') for x in range(32)])))
			paths = []

			if run_all:
				paths = ['bnroths/chicago-data/%s' % dataset]
				cnts = {}

			else:
				for month in date_list:
					year, month = month.split('-')
					paths.append('bnroths/chicago-data/%s/year=%s/month=%s' % (dataset, year, month))
				print paths
				cnts = datasets[dataset]['cnts'] 
				# exit(0)

			print paths
			for path in paths:
				ds = pq.ParquetDataset(
					path_or_paths=path,
					filesystem=S3FS, 
					validate_schema=False
					)

				columns = datasets[dataset]['columns']
				dt 		= columns[1]
				table 	= ds.read()
				df 		= table.to_pandas()
				print df.columns
				print df.head()
				df['dt'] = df[dt].astype(str).str[:7]
				
				
				dts = []
				groups = dict(list(df.groupby('dt')))
				print groups.keys()
				# exit(0)
				for group in groups:
					print group
					year, month = group.split('-')
					
					a = groups[group][['longitude', 'latitude']].to_json(orient='values')
					cnts[group] = groups[group].count()[0]
					dts.append(group)
					
					filename = '../data/%s/%s-%s/all.json' % (dataset, year, month)

					if not os.path.exists(os.path.dirname(filename)):
						try:
							os.makedirs(os.path.dirname(filename))
						except OSError as exc: # Guard against race condition
							if exc.errno != errno.EEXIST:
								raise

					with open(filename, 'w') as f:
						f.write(a)
							
					## write to s3
					s3.save_file_public(
						local='../data/%s/%s-%s/all.json' % (dataset, year, month),
						dataset=dataset, 
						dt="%s-%s" % (year, month), 
						filename='all.json'
					)
					db.update_col(dataset=dataset, col='cnts', update=json.dumps(cnts))
			
s3 = S3()
d = Download()
db = DynamoConn()
## saves raw
# handler(None, None)

## saves public
save_data(run_all=True)