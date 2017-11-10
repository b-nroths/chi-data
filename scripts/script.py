# Chicago, IL 60615
# 41.798133, -87.596405
# 41.798133, -87.596174
# -0.0002309999999994261
import json
with open('frontend/build/boundaries/Boundaries - City.json') as file:
	data = file.read() 
	data = json.loads(data)

lat_min = None
lat_max = None
lng_min = None
lng_max = None
num = 0

good = []
for row in data['features'][0]['geometry']['coordinates']:
	for point in row:
		print num
		num = 0
		print "HI"
		
		
		for p in point:
			num += 1
			lat, lng = p
			# good.append({'latitude': round(lng, 3), 'longitude': round(lat, 3)})
			good.append([round(lng, 3), round(lat, 3)])
			# print p
			if not lat_min:
				lat_min = lat
				lat_max = lat
				lng_min = lng
				lng_max = lng
			
			# print p
			if lat < lat_min:
				lat_min = lat
			if lat > lat_max:
				lat_max = lat
			if lng < lng_min:
				lng_min = lng
			if lng > lng_max:
				lng_max = lng
		# print 
		# with open('data.txt', 'w') as outfile:
		# 	json.dump(good, outfile)
		# exit(0)

print lat_min, lat_max, lng_min, lng_max
print lat_max - lat_min
print lng_max - lng_min

print lat_min - lng_min
print lat_max - lng_max

print (lat_min - lng_min)/-.00023
print (lat_max - lng_max)/-.00023

print 0.5*((lat_min - lng_min)/-.00023) * ((lat_max - lng_max)/-.00023)
# 158,670,381,416
# -0.343709082518
# -0.224905586989


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

x = -87.5241371039
y = 41.6445431225
polygon = Polygon(good)
while x >= -87.9401140825:
	x-= 0.01
	while y <= 42.023038587:
		y+= 0.01
		point = Point(x, y)
		print x, y
		print(polygon.contains(point))



