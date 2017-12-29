import sys, os
import os.path
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend/aws') 

from s3 import S3
from dynamo import DynamoConn
import pyarrow.parquet as pq
import s3fs, json
S3FS = s3fs.S3FileSystem()

s3 = S3()
db = DynamoConn()

dates = {}
datasets = db.get_datasets()
for dataset in datasets:
	dataset = 'crimes'
	print dataset
	ds = pq.ParquetDataset(
		path_or_paths='bnroths/chicago-data/%s' % (dataset), 
		filesystem=S3FS, 
		validate_schema=False)

	# print datasets[dataset]['columns']
	# print type(datasets[dataset]['columns'])
	columns = datasets[dataset]['columns']
	# exit(0)
	# try:
	columns = ['longitude', 'latitude', 'date']
	dt = columns[2]
	table = ds.read()
	# dt = columns[1]
	df = table.to_pandas()
	df['dt'] = df[dt].str[:7]
	# df.set_index(dt)
	# df.columns
	# print df.head()
	cnts = {}
	dts = []
	groups = dict(list(df.groupby('dt')))
	for group in groups:
		year, month = group.split('-')
		# print type(group)
		# # groups.get_group(group)
		a = groups[group][['longitude', 'latitude']].to_json(orient='values')
		# print a
		cnts[group] = groups[group].count()[0]
		dts.append(group)
		# print groups[group].count()
		filename = '../data/%s/%s/%s.json' % (dataset, year, month)

		if not os.path.exists(os.path.dirname(filename)):
			try:
				os.makedirs(os.path.dirname(filename))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise

		with open(filename, 'w') as f:
			f.write(a)
				
	# except:
	# 	print "ERROR", dataset
	# 	pass
	# print df.describe()
	db.update_col(dataset=dataset, col='cnts', update=json.dumps(cnts))
	db.update_col(dataset=dataset, col='dts', update=json.dumps(sorted(dts)))
	print cnts
	print dts
	# exit(0)	
# with open('../data/%s/%s.json' % (dataset, year), 'w') as f:
	# f.write(a)