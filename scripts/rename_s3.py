import boto3

class S3():
	def __init__(self):
		self.s3 	= boto3.client('s3')
		
	def list_files(self, dataset):
		res = self.s3.list_objects(
			Bucket='bnroths',
			Prefix='chicago-data/%s' % dataset,
		)
		fnames = []
		for file in res['Contents']:
			fnames.append(file['Key'])
		return fnames

	def save_file(self, filename):
		self.s3.upload_file(filename, 'bnroths', 'chicago-data/%s' % filename.replace('-', '/'))
		return True

s = S3()

for file in s.list_files('crimes'):
	print file
	folder, dataset, year, month, day = file.split('/')
	print folder, dataset, year, month, day
	
	s.s3.copy_object(Bucket="bnroths", CopySource={'Bucket': 'bnroths', 'Key': file}, Key='%s/%s-day/year=%s/month=%s/%s' % (folder, dataset, year, month, day))
	s.s3.delete_object(Bucket="bnroths", Key=file)
	# exit(0)