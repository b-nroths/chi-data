import requests as r

top_ten = ['The Loop',
	'Streeterville',
	'O\'Hare International Airport',
	'South Loop',
	'River North',
	'Bronzeville',
	'Near North',
	'West Loop Gate',
	'West Town',
	'Archer Heights',
	'Hyde Park']

datasets = [
	'final-jobs-eigs-chicago-S000'
]

# 
for neighborhood in top_ten:
	line = neighborhood + " & "
	for i in range(14):
		for dataset in datasets:
			year = i + 2002
			url = 'http://chicago.bnroths.com/data/%s/%s/1.json' % (dataset, year)
			res = r.get(url).json()
			num = res['data'][neighborhood]['real']
			# print num
			# print type(num)
			# print 0.01*num
			line += "%s & " % str(round(0.001*num, 3))
	print line + "\\\\ \n"