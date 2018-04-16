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

top_ten = [
	'Logan Square',	
	'Englewood',	
	'Gresham',
	'West Rogers Park',
	'Little Village',
	'Albany Park',
	'Portage Park',
	'Archer Heights',
	'Brighton Park',
	'Back of the Yards'
]
datasets = [
	'final-homes-eigs-chicago-S000'
	# 'final-jobs-eigs-chicago-SE01',
	# 'final-jobs-eigs-chicago-SE02',
	# 'final-jobs-eigs-chicago-SE03',
	# 'SE01': 'salary_group_1',
	# 'SE02': 'salary_group_2',
	# 'SE03': 'salary_group_3',
]

# 

for dataset in datasets:
	print dataset
	line = ""
	for neighborhood in top_ten:
		line += neighborhood + " & "
		for i in range(14):
			year = i + 2002
			url = 'http://chicago.bnroths.com/data/%s/%s/1.json' % (dataset, year)
			res = r.get(url).json()
			
			try:
				num = res['data'][neighborhood]['real']
			except:
				num = 0
			# print num
			# print type(num)
			# print 0.01*num
			# float(("%0.2f"%a))
			line += "%0.3f & " % round(0.001*num, 3)
		line += "\n"
	print line + "\\\\ \n"