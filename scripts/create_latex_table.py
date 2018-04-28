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

# young age
top_ten = [
'Logan Square',
'Little Village',
'Gresham',
'Englewood',
'Archer Heights',
'Lake View',
'Brighton Park',
'West Rogers Park',
'Rogers Park',
'Marquette Park',
'Gage Park',
]
# old age

datasets = [
	'final-homes-eigs-chicago-S000'
	# 'final-homes-eigs-chicago-SA01',
	# 'final-homes-eigs-chicago-SA03',
	# 'final-homes-eigs-chicago-SE01',
	# 'final-homes-eigs-chicago-SE03',
	# 'final-jobs-eigs-chicago-SE01',
	# 'final-jobs-eigs-chicago-SE02',
	# 'final-jobs-eigs-chicago-SE03',
	# 'SE01': 'salary_group_1',
	# 'SE02': 'salary_group_2',
	# 'SE03': 'salary_group_3',
]

# 
def keyfunction(k):
    return d[k]

for dataset in datasets:
	print dataset
	url = 'http://chicago.bnroths.com/data/%s/2015/1.json' % (dataset)
	res = r.get(url).json()

	places = {}
	for a in res['data']:
		places[a] = res['data'][a]['real']

	t = sorted(places.iteritems(), key=lambda x:-x[1])[:10]
	
	line = ""
	for neighborhood_val in t:
		neighborhood, val = neighborhood_val
		line += neighborhood + " & "
		datas = []
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
			# 
			datas.append(round(0.001*num, 3))
		datas.append(100.0 * (1.0*datas[-1]/datas[0] - 1))
		fdatas = [("%0.3f" % a) for a in datas]
		line += " & ".join(fdatas)
		line += "\n"
	print line + "\\\\ \n"