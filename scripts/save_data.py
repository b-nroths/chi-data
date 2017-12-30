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
	dataset = 'vacant_311'
	print dataset
	ds = pq.ParquetDataset(
		path_or_paths='bnroths/chicago-data/%s' % (dataset), 
		filesystem=S3FS, 
		validate_schema=False
		)

	columns = datasets[dataset]['columns']
	dt 		= columns[1]
	table 	= ds.read()
	df 		= table.to_pandas()
	print df.columns
	print df.head()
	df['dt'] = df[dt].astype(str).str[:7]
	
	cnts = {}
	dts = []
	groups = dict(list(df.groupby('dt')))
	print groups.keys()
	for group in groups:
		print group
		year, month = group.split('-')
		
		a = groups[group][['longitude', 'latitude']].to_json(orient='values')
		cnts[group] = groups[group].count()[0]
		dts.append(group)
		
		filename = '../data/%s/%s/%s.json' % (dataset, year, month)

		if not os.path.exists(os.path.dirname(filename)):
			try:
				os.makedirs(os.path.dirname(filename))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise

		with open(filename, 'w') as f:
			f.write(a)
				
		db.update_col(dataset=dataset, col='cnts', update=json.dumps(cnts))
		db.update_col(dataset=dataset, col='dts', update=json.dumps(sorted(dts)))
	
	print cnts
	print dts
	# exit(0)	
