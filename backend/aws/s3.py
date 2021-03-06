import os, ast, sys, json, time, pprint, uuid, datetime, re, gzip, io, csv
from dateutil import parser

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored")) 

import requests, boto3
from boto3.dynamodb.conditions import Key
import s3fs
import pyarrow as pa
import pyarrow.parquet as pq

class S3():
	def __init__(self):
		self.s3 	= boto3.client('s3')
		
	def list_files(self, dataset):
		get_files = True
		# marker = None
		while get_files:

			res = self.s3.list_objects(
				Bucket='bnroths',
				Prefix='chicago-data/%s' % dataset,
				# Marker=marker
			)
			fnames = []
			for file in res['Contents']:
				fnames.append(file['Key'].split('/')[-1].replace('.parquet', ''))

			print res['Marker']
			if res['Marker']:
				marker = res['Marker']
			else:
				get_files = False

			return fnames

	def save_file_lehd(self, filename, dataset_name, year):
		# print filename, dataset_name, year
		self.s3.upload_file(filename, 
			'bnroths', 
			'chicago-data/%s/year=%s/%s' % (dataset_name, year, filename))
		return True

	def save_file(self, filename, dataset_name, year, month):
		# print filename, dataset_name, year
		self.s3.upload_file(filename, 
			'bnroths', 
			'chicago-data/%s/year=%s/month=%s/%s.parquet' % (dataset_name, year, month, month))
		return True

	def save_file_public(self, local, dataset, dt, filename):
		# print local, dataset, dt, filename
		# print filename, dataset_name, year
		self.s3.upload_file(local, 
			'chicago.bnroths.com', 
			'data/%s/%s/%s' % (dataset, dt, filename))
		return True

	def rec_s3_dynamo(self, dataset):
		'''
		Some datasets were deleted from s3 but are still in dynamoDB cnt
		'''
		pass

	def get_df(self, dataset, columns='columns_short', year='2014'):
		s3 = s3fs.S3FileSystem()
		ds = pq.ParquetDataset(path_or_paths='bnroths/chicago-data/%s/year=%s' % (dataset, year), filesystem=s3, validate_schema=False)
		table = ds.read()#columns=datas[dataset][columns])
		df = table.to_pandas()
		return df


	
		