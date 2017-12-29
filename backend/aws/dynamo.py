import requests, boto3, json
from boto3.dynamodb.conditions import Key

class DynamoConn():
	def __init__(self):
		self.dynamodb 	= boto3.resource('dynamodb')
		self.table 		= self.dynamodb.Table('chicago-data')

	def put_item(self, json_data):
		## does not have to be json
		res = self.table.put_item(Item=json_data)
		
	def get_all(self, data_source=None):
		if data_source:
			response = self.table.scan(
				FilterExpression=Key('data_source').eq('plenario')
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
			row = {}
			row['name'] 			= dataset_item['name']
			row['columns'] 			= dataset_item['columns']
			row['dataset_start'] 	= dataset_item['dataset_start']
			row['example_data'] 	= json.loads(dataset_item['example_data'])
			row['data_source'] 		= dataset_item['data_source']
			row['description'] 		= dataset_item['description']
			row['cnts'] 			= json.loads(dataset_item['cnts'])
			row['dts'] 				= json.loads(dataset_item['dts'])
			res[dataset_item['dataset']] = row
		return res

	def update_col(self, dataset, col, update):
		item = self.get(dataset)
		item[col] = update
		self.put_item(item)
		return True

	def dump(self):
		with open('datasets.json', 'w') as f:
			f.write(json.dumps(self.get_all(), indent=4, sort_keys=True))
		return True

	def save_all(self):
		with open('datasets.json', 'r') as f:
			parsed = json.load(f)
			for row in parsed:
				print row
				self.put_item(row)

# DynamoConn().dump()
# DynamoConn().save_all()