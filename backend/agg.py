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

db   = DynamoConn()
d    = Download()
s3   = S3()
S3FS = s3fs.S3FileSystem()

def handler(event, context):

	data = {}
	for dataset_item in db.get_all():
		# print dataset_item
		dataset    = dataset_item['dataset']
		columns    = dataset_item['columns']
		map_type   = dataset_item['map_type']
		if map_type != 'arc' and dataset != '' and dataset == 'lehd_rac':
			print dataset, columns
		
			paths = ['bnroths/chicago-data/%s' % dataset]
		
			for path in paths:
				ds = pq.ParquetDataset(
					path_or_paths=path,
					filesystem=S3FS, 
					validate_schema=False
					)
				# print datasets[dataset].keys()
				columns 	= dataset_item['columns']
				datatypes 	= json.loads(dataset_item['sub_data'])
				years 		= [x + 2002 for x in range(14)]
				print datatypes
				col 		= columns[0]
				table 	= ds.read()
				df 		= table.to_pandas()
				
				# exit(0)
				# df['dt'] = df[dt].astype(str).str[:7]
				chi_data = df[df[columns[0]].isin(chicago_tracts)]
				year_data = chi_data.groupby([col, 'year']).sum().to_dict()
				# print year_data.columns
				# print year_data.head()

				# for year in years:
					# chi_data.loc

				for index, row in year_data.iteritems():
					print index, row

				print year_data.keys()
				# exit(0)

				for tract in chicago_tracts:
					tract_data = {}
					for stat in datatypes:
						stat_key = stat['key']
						tract_data[stat_key] = {'data': [], 'meta': stat}
						stat = stat['key']
						for year in years:
							tract_data[stat_key]['data'].append({'year': year, 'cnt': year_data[stat_key][(tract, year)]})
							# print year, tract, stat, year_data[stat][(tract, year)]
					filename = '%s.json' % tract
					print filename
					# exit(0)
					with open(filename, 'w') as f:
						f.write(json.dumps(tract_data))
					s3.save_file_public(
						local=filename,
						dataset='tract_data', 
						dt='lehd_rac', 
						filename=filename
					)
					tract_data = {}
					# exit(0)




				exit(0)
				# print year_data.head()
				for index, row in chi_data.iterrows():
					print index, row
				# print year_data
				exit(0)
				vals = []
				final = {}
				for stat in year_data.keys():
					# print year_data[stat].to_json()
					file_data = {}
					
					final['data'] = json.loads(year_data[stat].to_dict())
					final['meta'] = {
						'min': year_data[stat].min(),
						'top': sorted(year_data[stat])[-15],
						'max': year_data[stat].max()
					}
					with open('%s.json' % stat, 'w') as f:
						f.write(json.dumps(final))


					s3.save_file_public(
						local='%s.json' % stat,
						dataset=dataset, 
						dt=year, 
						filename='%s.json' % stat
					)
					os.remove('%s.json' % stat)
				
				
		# 		groups = dict(list(df.groupby('dt')))
		# 		print groups.keys()
		# 		# exit(0)
		# 		for group in groups:
		# 			print group, type(group)
		# 			if group != "None": # there is seriously a blank date
		# 				year, month = group.split('-')
						
		# 				a = groups[group][['longitude', 'latitude']].to_json(orient='values')
		# 				if dataset == 'building_permits':
		# 					if group >= '2016':
		# 						cnts[group] = groups[group].count()[0]
		# 				elif dataset == 'business_liscenses':
		# 					if group >= '2002':
		# 						cnts[group] = groups[group].count()[0]
		# 				else:
		# 					cnts[group] = groups[group].count()[0]
						
		# 				filename = '../data/%s/%s-%s/all.json' % (dataset, year, month)

		# 				if not os.path.exists(os.path.dirname(filename)):
		# 					try:
		# 						os.makedirs(os.path.dirname(filename))
		# 					except OSError as exc: # Guard against race condition
		# 						if exc.errno != errno.EEXIST:
		# 							raise

		# 				with open(filename, 'w') as f:
		# 					f.write(a)
								
		# 				## write to s3
		# 				s3.save_file_public(
		# 					local='../data/%s/%s-%s/all.json' % (dataset, year, month),
		# 					dataset=dataset, 
		# 					dt="%s-%s" % (year, month), 
		# 					filename='all.json'
		# 				)
		# 				db.update_col(dataset=dataset, col='cnts', update=json.dumps(cnts))
	return None
	
handler(None, None)
