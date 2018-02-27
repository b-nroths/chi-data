import json, sys
sys.path.append('/Users/benjamin/Desktop/repos/chi-data/backend') 
from config import cook_tracts, chicago_tracts
# u'properties': {u'name10': u'6309', u'tractce10': u'630900', u'notes': None, u'namelsad10': u'Census Tract 6309', u'countyfp10': u'031', u'commarea_n': 63.0, u'statefp10': u'17', u'hash': u'5c65a1dbc73bf2ce74cb0510acd3a6fe', u'commarea': u'63', u'geoid10': u'17031630900'}}
# 17031010100
features = []
with open('../data/boundaries/tracts_il_raw.json') as f:
	il_tracts = json.loads(f.read())
	for a in il_tracts['features']:
		# if a['properties']['GEO_ID'][-11:] in chicago_tracts:
		a['properties']['geoid10'] = a['properties']['GEO_ID'][-11:]
		features.append(a)

il_tracts['features'] = features
with open('../data/boundaries/tracts_il.json', 'w') as outfile:
	json.dump(il_tracts, outfile)