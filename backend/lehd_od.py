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

def handler(event, context):
	base_url = 'https://lehd.ces.census.gov/data/lodes'
	versions = ['LODES7'] # 'LODES6', 'LODES5'
	states	 = ['il']
	files 	 = ['wac']#, 'wac', 'od']
	print versions, states, files
	for version in versions:
		for state in states:
			for file in files:
				example_data = [json.loads(db.get(dataset=file)['example_data'])]
				schema = ingest_data(example_data).schema
				# print schema
				print example_data
				url = '%s/%s/%s/%s' % (base_url, version, state, file)
				print url
				c = r.get(url).content
				soup = BeautifulSoup(c, "html.parser")
				for link in soup.findAll('a', attrs={'href': re.compile("gz")}):
					print link.get('href').split('_')[4][:4]
					if link.get('href').split('_')[4][:4] in ('2010', '2011', '2012', '2013', '2014', '2015'):
						file_url = url + '/' + link.get('href')
						print version, state, file, file_url
						response = r.get(file_url).content
						# print type(response)
						df = pd.read_csv(file_url, compression='gzip')

						if file in ('rac', 'od'):
							df['h_tract'] = df['h_geocode'].astype(str).str[:11]
						if file in ('wac', 'od'):
							df['w_tract'] = df['w_geocode'].astype(str).str[:11]
						print df.head()
						# print df.iloc[0].to_json()
						# db.update_col('wac', 'example_data', df.iloc[0].to_json())
						try:
							table = pa.Table.from_pandas(df, schema=schema)
							print "\n"
							print table.schema
							print type(table.schema)
							# exit(0)
							last_part = file_url.split('/')[-1].split('.')[0]
							# print last_part

							state, file_type, part, job_type, year = last_part.split('_')
							filename = '%s.parquet' % (last_part)
							print df.head()
							# exit(0)
							table = pa.Table.from_pandas(df, schema=schema)
							pq.write_table(table, filename)
							s3.save_file_lehd(
								filename=filename, 
								dataset_name=file, 
								year=year
							)
							os.remove(filename)
						except:
							pass
					# print "bye"
					# exit(0)

	return {"result": "GTG"}


def save_data(dataset='od_work', year='2014', load_pickle=False):
	chi_tracts = r.get('https://s3.amazonaws.com/chicago.bnroths.com/data/boundaries/tracts.json').json()
	centroids = {}
	for tract in chi_tracts['features']:
		poly = geometry.Polygon(tract['geometry']['coordinates'][0][0])
		centroids[tract['properties']['geoid10']] = [poly.centroid.x, poly.centroid.y]
		
	for dataset in [dataset]:
		for year in range(14):
			year += 2002
			# year += 2002
			
			path = 'bnroths/chicago-data/od/year=%s/il_od_main_JT00_%s.parquet' % (year, year)
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
				

			# print final
			

			# {source: [-118.34921704225347, 33.8301492957746], 
			#   target: [-95.38370214285715, 29.82417309523809], 
			#   value: -3073, 
			#   gain: -1, 
			#   quantile: 3}
			all_arcs = []
			for tract in chi_tracts['features']:
				h_tract = tract['properties']['geoid10']
				arcs = []
				for arc in final[h_tract]:
					w_tract  = arc.keys()[0] 
					value    = arc.values()[0]
					this_arc = {
						'sourcePosition': centroids[h_tract],
						'targetPosition': centroids[w_tract],
						'value': value
					}
					if value >= 25:
						print this_arc
						arcs.append(this_arc)
						all_arcs.append(this_arc)
				tract['properties']['arcs'] = arcs
				# tract['properties']
			with open('all.json', 'w') as f:
				f.write(json.dumps(chi_tracts))

			with open('all_arcs.json', 'w') as f:
				f.write(json.dumps(all_arcs))

			s3.save_file_public(local='all.json', dataset=dataset, dt=year, filename='all.json')
			s3.save_file_public(local='all_arcs.json', dataset=dataset, dt=year, filename='all_arcs.json')
# handler(None, None)
save_data()
