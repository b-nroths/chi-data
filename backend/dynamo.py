import requests, boto3
from boto3.dynamodb.conditions import Key

class dynamoConn():
	def __init__(self):
		self.dynamodb 	= boto3.resource('dynamodb')
		self.table 		= self.dynamodb.Table('chicago-data')

	def put_item(self, json_data):
		res = self.table.put_item(Item=json_data)
		
	def get_all(self, data_source=None):
		if data_source:
			response = self.table.scan(
				FilterExpression=Key('data_source').eq('plenario')
			)
		else:
			response = table.scan()

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