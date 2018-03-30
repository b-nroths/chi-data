import json, sys
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend') 
from config import cook_tracts, chicago_tracts, msa_tracts
# u'properties': {u'name10': u'6309', u'tractce10': u'630900', u'notes': None, u'namelsad10': u'Census Tract 6309', u'countyfp10': u'031', u'commarea_n': 63.0, u'statefp10': u'17', u'hash': u'5c65a1dbc73bf2ce74cb0510acd3a6fe', u'commarea': u'63', u'geoid10': u'17031630900'}}
# 17031010100
features = []

with open('../data/boundaries/tracts_zillow.json') as f:
	il_tracts = json.loads(f.read())
	print "il"
	for a in il_tracts['features']:
		a['properties']['geoid10'] = a['properties']['Name']
		features.append(a)

with open('../data/boundaries/tracts_zillow_final.json', 'w') as outfile:
	json.dump(il_tracts, outfile)

exit(0)
with open('../data/boundaries/tracts_il_raw.json') as f:
	il_tracts = json.loads(f.read())
	print "il"
	for a in il_tracts['features']:
		if a['properties']['GEO_ID'][-11:] in msa_tracts:
			a['properties']['geoid10'] = a['properties']['GEO_ID'][-11:]
			features.append(a)

with open('../data/boundaries/tracts_in_raw.json') as f:
	in_tracts = json.loads(f.read())
	print "in"
	for a in in_tracts['features']:
		print a
		if a['properties']['GEOID'][-11:] in msa_tracts:
			a['properties']['geoid10'] = a['properties']['GEOID'][-11:]
			features.append(a)

with open('../data/boundaries/tracts_wi_raw.json') as f:
	wi_tracts = json.loads(f.read())
	print "wi"
	for a in wi_tracts['features']:
		if a['properties']['GEOID'][-11:] in msa_tracts:
			a['properties']['geoid10'] = a['properties']['GEOID'][-11:]
			features.append(a)

il_tracts['features'] = features
with open('../data/boundaries/tracts_msa.json', 'w') as outfile:
	json.dump(il_tracts, outfile)

# exit(0)
# # https://www.census.gov/geo/maps-data/maps/2010ref/st17_tract.html
# # http://mapshaper.org/
# # https://www.census.gov/geo/maps-data/data/cbf/cbf_tracts.html
import requests as r
counties = {
	'cook': 'https://www2.census.gov/geo/maps/dc10map/tract/st17_il/c17031_cook/DC10CT_C17031_CT2MS.txt', #
	'dekalb': 'https://www2.census.gov/geo/maps/dc10map/tract/st17_il/c17037_dekalb/DC10CT_C17037_CT2MS.txt', #
	'dupage': 'https://www2.census.gov/geo/maps/dc10map/tract/st17_il/c17043_dupage/DC10CT_C17043_CT2MS.txt', #
	'grundy': 'https://www2.census.gov/geo/maps/dc10map/tract/st17_il/c17063_grundy/DC10CT_C17063_CT2MS.txt',
	'kane': 'https://www2.census.gov/geo/maps/dc10map/tract/st17_il/c17089_kane/DC10CT_C17089_CT2MS.txt',
	'kendall': 'https://www2.census.gov/geo/maps/dc10map/tract/st17_il/c17093_kendall/DC10CT_C17093_CT2MS.txt',
	'lake': 'https://www2.census.gov/geo/maps/dc10map/tract/st17_il/c17097_lake/DC10CT_C17097_CT2MS.txt',
	'mchenry': 'https://www2.census.gov/geo/maps/dc10map/tract/st17_il/c17111_mchenry/DC10CT_C17111_CT2MS.txt',
	'will': 'https://www2.census.gov/geo/maps/dc10map/tract/st17_il/c17197_will/DC10CT_C17197_CT2MS.txt',
	# ## wi
	'kenosha': 'https://www2.census.gov/geo/maps/dc10map/tract/st55_wi/c55059_kenosha/DC10CT_C55059_CT2MS.txt',
	# ## in
	'jasper': 'https://www2.census.gov/geo/maps/dc10map/tract/st18_in/c18073_jasper/DC10CT_C18073_CT2MS.txt',
	'lake': 'https://www2.census.gov/geo/maps/dc10map/tract/st18_in/c18089_lake/DC10CT_C18089_CT2MS.txt',
	'newton': 'https://www2.census.gov/geo/maps/dc10map/tract/st18_in/c18111_newton/DC10CT_C18111_CT2MS.txt',
	'porter': 'https://www2.census.gov/geo/maps/dc10map/tract/st18_in/c18127_porter/DC10CT_C18127_CT2MS.txt'
}	
import time
msa_tracts = []
for county in counties:
	print county
	res = r.get(counties[county])
	# time.sleep(5)
	print res.status_code

	print res.content
	for line in res.content.split('\n'):
		print line 
		line = line.split(';')
		print len(line)
		if len(line) == 4:
			print line[1]
			if len(line[1]) == 11:
				if line[1] == '17097860811':
					print "HIHIHI"
				msa_tracts.append(line[1])
print msa_tracts
print len(msa_tracts)
