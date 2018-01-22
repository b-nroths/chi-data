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
import requests as r

from aws.dynamo import DynamoConn
from bs4 import BeautifulSoup
from aws.s3 import S3
from config import chicago_tracts
import s3fs, json

from json2parquet import load_json, ingest_data, write_parquet
from shapely import geometry
	

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



def save_data(datasets=['lehd_od_home', 'lehd_od_work'], year='2014', load_pickle=False):
	chi_tracts = r.get('https://s3.amazonaws.com/chicago.bnroths.com/data/boundaries/tracts.json').json()
	centroids = {}
	for tract in chi_tracts['features']:
		poly = geometry.Polygon(tract['geometry']['coordinates'][0][0])
		centroids[tract['properties']['geoid10']] = [poly.centroid.x, poly.centroid.y]
		
	for dataset in datasets:
		for year in range(14):
			year += 2002
			# year += 2002
			
			path = 'bnroths/chicago-data/lehd_od/year=%s/il_lehd_od_main_JT00_%s.parquet' % (year, year)
			print dataset, year, path
			ds = pq.ParquetDataset(
				path_or_paths=path,
				filesystem=S3FS, 
				validate_schema=False
			)
			# print ds
			table 	= ds.read()
			df 		= table.to_pandas()
			# print df.head()
			df = df[df['h_tract'].isin(chicago_tracts)]
			df = df[df['w_tract'].isin(chicago_tracts)]
			df = df.groupby(['h_tract', 'w_tract'])['S000'].sum()
			# print df.set_index('h_tract').to_json()
			final = {}
			for i, v in df.iteritems():
				h, w = i
				if h in final:
					final[h].append({w: v})
				else:
					final[h] = [{w: v}]
				
			all_arcs = []
			for tract in chi_tracts['features']:
				h_tract = tract['properties']['geoid10']
				arcs = []
				values   = []
				for arc in final[h_tract]:
					w_tract  = arc.keys()[0] 
					value    = arc.values()[0]
					this_arc = {
						'sourcePosition': centroids[h_tract],
						'targetPosition': centroids[w_tract],
						'value': value
					}
					if value >= 25:
						# print this_arc
						values.append(value)
						arcs.append(this_arc)
						all_arcs.append(this_arc)
				tract['properties']['arcs'] = arcs
				# print values
				try:
					tract['properties']['max_value'] = max(values)
				except:
					tract['properties']['max_value'] = 0

				# tract['properties']
			with open('all.json', 'w') as f:
				f.write(json.dumps(chi_tracts))

			with open('all_arcs.json', 'w') as f:
				f.write(json.dumps(all_arcs))

			s3.save_file_public(local='all.json', dataset=dataset, dt=year, filename='all.json')
			s3.save_file_public(local='all_arcs.json', dataset=dataset, dt=year, filename='all_arcs.json')
# handler(None, None)
save_data()
