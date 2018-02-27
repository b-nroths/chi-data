import sys, os, json
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend') 
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend/aws') 
from s3 import S3
from dynamo import DynamoConn
import pyarrow.parquet as pq
import pandas as pd
import numpy as np
import s3fs
import decimal
from config import cook_tracts, chicago_tracts
arrow_s3fs = s3fs.S3FileSystem()
s3 = S3()
d = DynamoConn()

dataset_names = {
	# 'eigs': {
	# 	'dataset': 'JT00',
	# 	'stat': 'S000',
	# 	'boundaries': chicago_tracts,
	# 	'boundary': 'chicago'
	# },
	'eigs-cook': {
		'dataset': 'JT00',
		'stat': 'S000',
		'boundaries': cook_tracts,
		'boundary': 'cook'
	}
}

for dataset_name in dataset_names:
	all_of_the_keys = {}

	for i in range(14):
		year = 2002 + i
		print year
		ds = pq.ParquetDataset(
			path_or_paths='bnroths/chicago-data/lehd_od/year=%s/il_lehd_od_main_%s_%s.parquet' % (year, dataset_names[dataset_name]['dataset'], year), 
			filesystem=arrow_s3fs, 
			validate_schema=False
		)

		table = ds.read()
		df = table.to_pandas()
		if dataset_names[dataset_name]['boundary'] in ('chicago', 'cook'):
			df = df[df['h_tract'].isin(dataset_names[dataset_name]['boundaries'])]
			df = df[df['w_tract'].isin(dataset_names[dataset_name]['boundaries'])]

		print (set(df.h_tract) - set(df.w_tract))
		print (set(df.w_tract) - set(df.h_tract))
		diff = set(df.h_tract) - set(df.w_tract)
		for tract in diff:
			df = df[df.h_tract != tract]

		pivot = pd.pivot_table(df, values=dataset_names[dataset_name]['stat'], columns=['w_tract'], index=['h_tract'], aggfunc=np.sum)

		pivot = pivot.fillna(0)
		print pivot.shape

		w, v = np.linalg.eig(pivot)

		eigs = []
		idx = w.argsort()[::-1]
		eigenValues = w[idx]
		eigenVectors = v[:,idx]
		sub_data = []
		for i in range(10):
			print i
			eigenvalue_i = i+1
			val = round(eigenValues[i], 4)
			vector = eigenVectors[:, i]
			sub_data.append({
				"name": "Eigenvalue %s" % eigenvalue_i,
				"value": round(val, 2),
				"key": str(eigenvalue_i)
			})
			transformed = [round(1000*x, 1) for x in np.absolute(vector)]
			eig = {
				"row": i,
				"value": val,
				"vector": transformed,
				"columns": pivot.columns
			}
			eigs.append(eig)
			tracts = {}
			for i, column in enumerate(pivot.columns):
				tracts[column] = transformed[i]
					
			final = {
				"data": tracts,
				"meta": {
					"max": max(tracts.values()),
					"min": min(tracts.values()),
					"top": sorted(tracts.values())[-15]
				}
			}
		
			stat = eigenvalue_i

			with open('%s.json' % stat, 'w') as f:
				f.write(json.dumps(final))

			s3.save_file_public(
				local='%s.json' % stat,
				dataset=dataset_name, 
				dt=year, 
				filename='%s.json' % stat
			)
			os.remove('%s.json' % stat)

			all_of_the_keys["%s" % year] = sub_data

		## update dynamo metadata
		metadata = d.get(dataset=dataset_name)
		metadata['table'] = json.dumps(all_of_the_keys)
		d.put_item(metadata)

print all_of_the_keys
