import requests, boto3, json
from boto3.dynamodb.conditions import Key

class DynamoConn():
	def __init__(self):
		self.dynamodb 	= boto3.resource('dynamodb')
		self.table 		= self.dynamodb.Table('chicago-data')

	def put_item(self, json_data):
		## does not have to be json
		res = self.table.put_item(Item=json_data)
		
	def get_all(self, data_source=None, show=True):
		if data_source:
			response = self.table.scan(
				FilterExpression=Key('source').eq(data_source)
			)
		else:
			response = self.table.scan()

		return response['Items']

	def get(self, dataset):
		response = self.table.get_item(
		   Key={
				'dataset': dataset
			}
		)
		if 'Item' in response:
			return response['Item']
		else:
			return None

	def get_datasets(self):
		res = {}
		for dataset_item in self.get_all():
			print dataset_item['name']
			if dataset_item['show']:
				print dataset_item
				row = {}
				row['name'] 					= dataset_item['name']
				row['columns'] 					= dataset_item['columns']
				row['order']					= int(dataset_item['order'])
				row['dataset_start'] 			= dataset_item['dataset_start']
				row['example_data'] 			= json.loads(dataset_item['example_data'])
				row['description'] 				= dataset_item['description']
				row['cnts'] 					= json.loads(dataset_item['cnts'])
				row['sub_data'] 				= json.loads(dataset_item['sub_data'])
				row['last_updated'] 			= dataset_item['last_updated']
				row['source'] 					= dataset_item['source']
				row['map_type']					= dataset_item['map_type']
				row['table'] 					= json.loads(dataset_item['table'])
				row['boundary'] 				= dataset_item['boundary']
				res[dataset_item['dataset']] 	= row
				print row['order']
		return res

	def update_col(self, dataset, col, update):
		item = self.get(dataset)
		item[col] = update
		self.put_item(item)
		return True

	def dump(self):
		with open('datasets.json', 'w') as f:
			f.write(json.dumps(self.get_datasets(), indent=4, sort_keys=True))
		return True

	def save_all(self):
		with open('datasets.json', 'r') as f:
			parsed = json.load(f)
			for row in parsed:
				print row
				self.put_item(row)

# d = DynamoConn()
# data = d.get_datasets()
# for i, a in enumerate(data):
# 	print i, a['name']
# 	if not a['show']:
# 		print a
		# d.table.delete_item(Key={'dataset': a['dataset']})
	# exit(0)
	# d.
	#if 'eig' in a['name'].lower():
	#	a['source'] = 'lehd'
	#	a['dataset_long_name'] = None
	#	a['sub_data'] = json.dumps([{"name": "Eigenvalue 1", "key": "1"}, {"name": "Eigenvalue 2", "key": "2"}])
	#	d.put_item(a)
	#print "\n"
# DynamoConn().dump()
# DynamoConn().save_all()