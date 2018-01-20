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
				c = requests.get(url).content
				soup = BeautifulSoup(c, "html.parser")
				for link in soup.findAll('a', attrs={'href': re.compile("gz")}):
					print link.get('href').split('_')[4][:4]
					if link.get('href').split('_')[4][:4] in ('2010', '2011', '2012', '2013', '2014', '2015'):
						file_url = url + '/' + link.get('href')
						print version, state, file, file_url
						response = requests.get(file_url).content
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


def save_data(datasets=['wac'], year='2014', load_pickle=False):

	for dataset in datasets:
		for year in range(14):
			year += 2002
			# if year >= 2010:
			if dataset == 'wac':
				path = 'bnroths/chicago-data/%s/year=%s/il_wac_S000_JT00_%s.parquet' % (dataset, year, year)
			else:
				path = None
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
			if dataset == 'wac':
				col = 'w_tract'
			else:
				col = 'h_tract'
			chi_data = df[df[col].isin(chicago_tracts)]
			print 'start group by'
			# groups = dict(list(df.groupby('dt')))
			year_data = chi_data.groupby([col]).sum()#.to_json()
			# print year_data
			# print year_data.keys()
			# for k in year_data.keys():
				# print k
				# print k, year_data[k]['17031843600']
			# exit(0)
			# year_data = json.loads(year_data)
			# print year_data
			# with open('data.pickle', 'wb') as handle:
				# pickle.dump(year_data, handle)
			# keys = year_data.keys()

			 # writes files to
			vals = []
			final = {}
			for stat in year_data.keys():
				# print year_data[stat].to_json()
				file_data = {}
				# vals.append()
				## save file
				# print year_data[stat]
				# print type(year_data[stat])
				# exit(0)
				final['data'] = json.loads(year_data[stat].to_json())
				final['meta'] = {
					'min': year_data[stat].min(),
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
			# exit(0)
		# db.update_col(dataset=dataset, col='cnts', update=json.dumps(cnts))
		# ## create file if it doesn't exist
		# if not os.path.exists('data_temp/%s.json' % stat):
		# 	with open('data_temp/%s.json' % stat, 'w+') as f:
		# 		f.write(json.dumps({}))

		# with open('data_temp/%s.json' % stat, 'r+') as f:
		# 	file_data = json.loads(f.read())
		# 	file_data[year] = year_data[stat]
		# 	# need to write at beginning of file
		# 	f.seek(0)
		# 	f.write(json.dumps(file_data))
		# 	f.truncate()

# handler(None, None)
save_data()
