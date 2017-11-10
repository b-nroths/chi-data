import datetime
import random
import json

# base = datetime.datetime.today()
# date_list = [base - datetime.timedelta(days=x) for x in range(0, 100*365)]

# lt = {}
# for d in date_list:
# 	print str(d)[:10]
# 	lt[str(d)[:10]] = int(10000*random.random())

# with open('test.json', 'w') as f:
# 	f.write(json.dumps(lt))


with open('untitled.json') as f:
	text = f.read()


print len(json.loads(text))