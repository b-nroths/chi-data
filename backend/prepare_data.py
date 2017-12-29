from aws.s3 import S3

from data import datas, tracts
import pandas as pd
import pickle, json, os
import pyarrow.parquet as pq

def upload_data():
	# aws s3 sync build/ s3://chicago.bnroths.com --delete
	pass

def save_web_keys():
	keys = []
	for stat in ['rac']:
		for k in datas[stat]:
			for key in datas[stat]['web_columns']:
				keys.append({'key': key, 'name': datas[stat]['columns'][key]['name']})
		print keys
	with open('data_temp/tract_keys.json', 'wr+') as handle:
		handle.write(json.dumps(keys))

def save_year_data(year='2014', load_pickle=False):

	if load_pickle:
		with open('data.pickle', 'rb') as handle:
			year_data = pickle.load(handle)

	else:
		s3 = S3()
		print 'downloading'
		df = s3.get_df('rac', columns='web_columns', year=year)
		chi_data = df[df['h_tract'].isin(tracts)]
		print 'start group by'
		year_data = chi_data.groupby(['h_tract']).sum().to_json()
		year_data = json.loads(year_data)
		print year_data
		with open('data.pickle', 'wb') as handle:
			pickle.dump(year_data, handle)
	keys = year_data.keys()

	 # writes files to
	for stat in keys:
		print stat
		file_data = {}

		## create file if it doesn't exist
		if not os.path.exists('data_temp/%s.json' % stat):
			with open('data_temp/%s.json' % stat, 'w+') as f:
				f.write(json.dumps({}))

		with open('data_temp/%s.json' % stat, 'r+') as f:
			file_data = json.loads(f.read())
			file_data[year] = year_data[stat]
			# need to write at beginning of file
			f.seek(0)
			f.write(json.dumps(file_data))
			f.truncate()
			
## run all
# for year in ['2002']:#, '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012']:
	# print year
	# s3 = S3()
	# df = s3.get_df('rac', columns='web_columns', year=year)
	# df = 
	# print df
	# save_year_data(year=year, load_pickle=False)

# table2 = pq.read_table('data/food_inspections/year=2010/01.parquet')
# df = table2.to_pandas()
# print df.head()
s3 = S3()
print s3.get_df('food_inspections', year='2010').head()

