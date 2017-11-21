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

from dynamo import dynamoConn
from bs4 import BeautifulSoup
from s3 import S3

class Download():

	def __init__(self):
		self.name   = 'Ben'

	def download_data(self):
		return True

	def transform_json(self):
		return True

db = dynamoConn()
d  = Download()
s3 = S3()

def handler(event, context):
	base_url = 'https://lehd.ces.census.gov/data/lodes'
	versions = ['LODES7'] # 'LODES6', 'LODES5'
	states	 = ['il']
	files 	 = ['rac', 'wac', 'od']
	print versions, states, files
	for version in versions:
		for state in states:
			for file in files:
				url = '%s/%s/%s/%s' % (base_url, version, state, file)
				print url
				c = requests.get(url).content
				soup = BeautifulSoup(c, "html.parser")
				for link in soup.findAll('a', attrs={'href': re.compile("gz")}):
					if '2014' not in link.get('href'):
						file_url = url + '/' + link.get('href')
						print version, state, file, file_url
						response = requests.get(file_url).content
						# print type(response)
						df = pd.read_csv(file_url, compression='gzip')

						if file in ('rac', 'od'):
							df['h_tract'] = df['h_geocode'].astype(str).str[:11]
						if file in ('wac', 'od'):
							df['w_tract'] = df['w_geocode'].astype(str).str[:11]
						# print df.head()
						last_part = file_url.split('/')[-1].split('.')[0]
						# print last_part

						state, file_type, part, job_type, year = last_part.split('_')
						filename = '%s.parquet' % (last_part)
						table = pa.Table.from_pandas(df)
						pq.write_table(table, filename)
						s3.save_file(filename=filename, dataset_name=file, year=year)
						os.remove(filename)
					# print "bye"
					# exit(0)

	return {"result": "GTG"}

handler(None, None)

