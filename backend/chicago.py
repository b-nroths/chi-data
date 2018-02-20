# serverless deploy
# serverless invoke local --function chicago
import os, ast, sys, json, time, pprint, uuid, datetime, re, gzip, io, csv
from dateutil import parser

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored")) 

import pandas as pd
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests

from aws.dynamo import DynamoConn
from bs4 import BeautifulSoup
from aws.s3 import S3
from config import chicago_tracts
import s3fs, json

from json2parquet import load_json, ingest_data, write_parquet

from sodapy import Socrata
import geocoder
import pickle

class Download():

	def __init__(self):
		self.name   = 'Ben'

	def download_data(self):
		return True

	def transform_json(self):
		return True

db = DynamoConn()
d  = Download()
s3 = S3()
S3FS = s3fs.S3FileSystem()

datasets = {
		# 'building_permits': {'key': '9pkb-4fbf', 'date': '_issue_date'},
		# 'business_liscenses': {'key': 'r5kz-chrr', 'date': 'license_start_date'}  ## 900,000 rows,
		'business_grants': {'key': 'jp7n-tgmf', 'date': 'completion_date'}
	}
address_lookup = pickle.load(open("address_lookup.p", "rb" ))

def handler(event, context):
	client = Socrata("data.cityofchicago.org", None)

	num_records = 45000
	offset      = 0
	for dataset in datasets:
		# print dataset
		results = client.get(datasets[dataset]['key'], limit=num_records, offset=0)
		res = {}
		print json.dumps(results[0])
		# exit(0)
		new_rows = []
		while results:
			print len(results)
			offset += 1
			for i, row in enumerate(results):
				print i
				try:
					key = row[datasets[dataset]['date']][:7]
				except:
					print row

				if dataset == 'business_grants':
					address = row['address']
					g = geocoder.google(address)
					if address in address_lookup:
						lat, lng = address_lookup[address]
						print "lookup worked"
					else:
						try:
							lat, lng = g.latlng
							address_lookup[address] = [lat, lng]
						except:
							print address
							lat, lng = None, None
					row['latitude'] = lat
					row['longitude'] = lng
				year, month = key.split('-')
				row.pop('location', None)
				# if key not in res:
					# res[key] = []
				new_rows.append(row)
				# print row
				# exit(0)
			if len(results) == num_records:
				print offset*num_records
				results = client.get(datasets[dataset]['key'], limit=num_records, offset=offset*num_records)
			else:
				results = None


		table = ingest_data(new_rows)#, schema)
		print key, len(table.schema)
		print address_lookup
		if dataset == 'business_grants':
			pickle.dump(address_lookup, open('address_lookup.p', 'wb'))
		filename = 'all.parquet'
		write_parquet(table, filename)
		s3.save_file(
			filename, 
			dataset, 
			'2018',
			'01')
		# TODO remove data
		os.remove(filename)

	return {"result": "GTG"}


def save_data(run_all=True):

	for dataset_item in db.get_all(data_source='Chicago Data Portal'):
		print dataset_item
		dataset    = dataset_item['dataset']
		if dataset == 'business_grants':
			print dataset
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
				# print datasets[dataset].keys()
				columns = dataset_item['columns']
				dt 		= columns[1]
				table 	= ds.read()
				df 		= table.to_pandas()
				print df.columns
				print df.head()
				# exit(0)
				df['dt'] = df[dt].astype(str).str[:7]
				
				
				groups = dict(list(df.groupby('dt')))
				print groups.keys()
				# exit(0)
				for group in groups:
					print group, type(group)
					if group != "None": # there is seriously a blank date
						year, month = group.split('-')
						
						a = groups[group][['longitude', 'latitude']].to_json(orient='values')
						if dataset == 'building_permits':
							if group >= '2016':
								cnts[group] = groups[group].count()[0]
						elif dataset == 'business_liscenses':
							if group >= '2002':
								cnts[group] = groups[group].count()[0]
						else:
							cnts[group] = groups[group].count()[0]
						
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
	return None
	



handler(None, None)
save_data()
