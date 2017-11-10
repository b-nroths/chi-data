class kinesisConn():
	def __init__(self):
		self.kinesis = boto3.client('firehose')
	#
	def list_streams(self):
		res = self.kinesis.list_delivery_streams(
			Limit=100,
		)
		return res['DeliveryStreamNames']
	#
	def get_stream(self, dataset):
		res = self.kinesis.describe_delivery_stream(
			DeliveryStreamName=dataset,
		)
		return res['DeliveryStreamDescription']
	#
	def put_records(self, stream, records):
		res = self.kinesis.put_record_batch(
			DeliveryStreamName=stream,
			Records=records
		)
		return True
	#
	def delete_stream(self, dataset):
		res = self.kinesis.delete_delivery_stream(
			DeliveryStreamName=dataset
	)
	#
	def get_or_create(self, dataset):
		if dataset in self.list_streams():
			return True
		else:
			response = self.kinesis.create_delivery_stream(
				DeliveryStreamName=dataset,
				DeliveryStreamType='DirectPut',
				S3DestinationConfiguration={
					'RoleARN': 'arn:aws:iam::617449064033:role/firehose_delivery_role',
					'BucketARN': 'arn:aws:s3:::bnroths',
					'Prefix': 'chicago-data/%s/' % dataset,
					'BufferingHints': {'SizeInMBs': 50, 'IntervalInSeconds': 60 },
					'CompressionFormat': 'UNCOMPRESSED',
					'EncryptionConfiguration': {'NoEncryptionConfig': 'NoEncryption',},
					'CloudWatchLoggingOptions': {'Enabled': True, 'LogGroupName': '/aws/kinesisfirehose/%s' % dataset, 'LogStreamName': 'S3Delivery'}
				}
			)

# dt = parser.parse(row['properties']['date'])
# if dt >= date_max or not date_max:
# 	date_max = dt

# kinesisRecord = {'Data': b'%s\n' % json.dumps(row)}
# batch.append(kinesisRecord)
# if i % 100 == 0:
# 	k.put_records(stream=dataset, records=batch)
# 	batch = []
# k.put_records(stream=dataset, records=batch)