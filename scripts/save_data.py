import sys, os, datetime
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
	# print dataset
	if datasets[dataset]['source'] == 'Plenario':
		today      = datetime.datetime.today().date()
		date_list  = set([today.strftime('%Y-%m')]) 
		date_list.add((today-datetime.timedelta(days=32)).strftime('%Y-%m'))
		date_list  = sorted(list(set([(today - datetime.timedelta(days=x)).strftime('%Y-%m') for x in range(32)])))
		print date_list
		paths = []
		for month in date_list:
			year, month = month.split('-')
			paths.append('bnroths/chicago-data/%s/year=%s/month=%s' % (dataset, year, month))
		print paths
		# exit(0)
		for path in paths:
			ds = pq.ParquetDataset(
				path_or_paths=path,# 'bnroths/chicago-data/%s' % dataset,
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
			
			cnts = datasets[dataset]['cnts'] 
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
						
				## write to s3
				s3.save_file_public(
					local='../data/%s/%s/%s.json' % (dataset, year, month),
					dataset=dataset, 
					year=year, 
					filename='%s.json' % month
				)
				db.update_col(dataset=dataset, col='cnts', update=json.dumps(cnts))
		
		print cnts
		print dts
	# exit(0)	
