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

for file in s.list_files('rac'):
	print file
	new_file = file.replace('rac', 'lehd_rac')
	s.s3.copy_object(Bucket="bnroths", CopySource={'Bucket': 'bnroths', 'Key': file}, Key=new_file)
	s.s3.delete_object(Bucket="bnroths", Key=file)