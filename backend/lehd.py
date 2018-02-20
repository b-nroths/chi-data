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
	files 	 = [ 'lehd_rac', 'lehd_wac']#'lehd_od']#,
	print versions, states, files
	for version in versions:
		for state in states:
			for file in files:
				example_data = [json.loads(db.get(dataset=file)['example_data'])]
				print example_data
				schema = ingest_data(example_data).schema
				print schema
				url = '%s/%s/%s/%s' % (base_url, version, state, file.replace('lehd_', ''))
				c = requests.get(url).content
				soup = BeautifulSoup(c, "html.parser")
				print len(soup.findAll('a', attrs={'href': re.compile("gz")}))
				print soup.findAll('a', attrs={'href': re.compile("gz")})

				# fnames_s3 = s3.list_files(dataset='lehd_wac')
				# exit(0)
				for i, link in enumerate(sorted(soup.findAll('a', attrs={'href': re.compile("gz")}))):
					
					if link.get('href').split('_')[4][:4] in (
						'2002',
						'2003', 
						'2004', 
						'2005', 
						'2006', 
						'2007', 
						'2008',
						'2009',
						'2010', 
						'2011', 
						'2012', 
						'2013', 
						'2014', 
						'2015'):
						file_url = url + '/' + link.get('href')
						# if link.get('href').split('.')[0] not in fnames_s3:
							# exit(0)
						print i, link.get('href').split('_')[4][:4], version, state, file, file_url
						try:
							print file_url
							exit(0)
							response = requests.get(file_url).content
							# print type(response)
							df = pd.read_csv(file_url, compression='gzip')

							if file in ('lehd_rac', 'lehd_od'):
								df['h_tract'] = df['h_geocode'].astype(str).str[:11]
							if file in ('lehd_wac', 'lehd_od'):
								df['w_tract'] = df['w_geocode'].astype(str).str[:11]
							
							table = pa.Table.from_pandas(df, schema=schema)
							# exit(0)
							last_part = file_url.split('/')[-1].split('.')[0]
							# print last_part

							state, file_type, part, job_type, year = last_part.split('_')
							filename = '%s.parquet' % (last_part)
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
							print "Probably a blank file"
							pass
					# print "bye"
					# exit(0)

	return {"result": "GTG"}


def save_data(datasets=['lehd_wac'], year='2014', load_pickle=False):

	for dataset in datasets:
		for year in range(14):
			year += 2002
			# if year >= 2010:
			if dataset == 'lehd_wac':
				path = 'bnroths/chicago-data/%s/year=%s/il_wac_S000_JT00_%s.parquet' % (dataset, year, year)
				col = 'w_tract'
			elif dataset == 'lehd_rac':
				path = 'bnroths/chicago-data/%s/year=%s/il_lehd_rac_S000_JT00_%s.parquet' % (dataset, year, year)
				col = 'h_tract'
			print dataset, year, path
			ds = pq.ParquetDataset(
				path_or_paths=path,
				filesystem=S3FS, 
				validate_schema=False
			)
			# print ds
			table 	= ds.read()
			df 		= table.to_pandas()
			print df.head()
			# exit(0)
			
				
			chi_data = df[df[col].isin(chicago_tracts)]
			print 'start group by'
			
			year_data = chi_data.groupby([col]).sum()#.to_json()
			
			vals = []
			final = {}
			for stat in year_data.keys():
				# print year_data[stat].to_json()
				file_data = {}
				
				final['data'] = json.loads(year_data[stat].to_json())
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



handler(None, None)
# save_data()
