import psycopg2
import json
from datas import datas
import boto3
from datetime import datetime, timedelta
import time
from decimal import *
import numpy as np
import statsmodels.api as sm

import pandas as pd
import numpy as np
from fbprophet import Prophet

class DynamoDB():
	def __init__(self, debug=True):
		self.debug = debug
		self.dynamodb = boto3.resource('dynamodb')
		self.table = self.dynamodb.Table('dash')

	def put(self, item):
		if self.debug:
			print("\n")
			print(item)
			print(self.table.put_item(Item=item))
		else:
			self.table.put_item(Key=item['name'], Item=item)
		return True

class Postgres():

	def __init__(self, debug=False):
		self.debug = debug
		self.conn = psycopg2.connect(dbname="uchicago", 
										user="bnroths", 
										password="sF4fLshzyzfNgEC", 
										host="uchicago.ctluqxmlzcvq.us-east-1.rds.amazonaws.com", 
										port="5432",
										)
		self.conn.autocommit = True
		self.cur = self.conn.cursor()

	def list_tables(self):
		query = """
		SELECT tablename FROM pg_catalog.pg_tables WHERE tableowner='bnroths'
		"""
		return self.query_list(query)

	def execute(self, query):
		if self.debug:
			print(query)
		return self.cur.execute(query)

	def query_list(self, query):
		self.execute(query)
		return self.cur.fetchall()

	def delete_from_table(self, dataset_name):
		query = """
		DELETE FROM %s
		""" % dataset_name
		self.execute(query)
		return True

	def drop_table(self, table, schema="datasets"):
		query = """
		DROP TABLE IF EXISTS %s.%s 
		""" % (schema, table)
		self.cur.execute(query)

class Data:

	def __init__(self):
		self.hi 	= "ben"
		base 		= datetime.today()
		self.dts 	= [(base - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 417)]
		self.today 	= datetime.today()
		self.p 		= Postgres()
		self.d 		= DynamoDB()

	def run_all(self):
		for data_name in datas:
			print(data_name)
			t1 					= time.time()
			row 				= datas[data_name]
			row['name'] 		= data_name
			row['updated_at'] 	= str(datetime.now())
			data 				= self.p.query_list(row['query'])
			row['data'] 		= self.transform_data(data)
			row['results'] 		= self.return_data(row['data'])
			
			if row['query_current']:
				current_data 		= self.p.query_list(row['query_current'])
				row['current_data'] = self.return_current(current_data)
			else:
				row['current_data'] = None
			t2 = time.time()
			row['run_duration'] = int(round(t2 - t1, 2))
			print(row.keys())
			self.d.put(row)

		return json.dumps(row)
	## need to add 0 for days that return no results
	## convert to dictionary with keys as dates
	def transform_data(self, data):
		res = {}

		# convert date to string, int
		data_dict = {}
		for row in data:
			# print row
			dt, amt = row
			data_dict[str(dt)] = int(amt)

		for dt in self.dts:
			if dt in data_dict:
				res[dt] = data_dict[dt]
			else:
				res[dt] = 0
		
		return res

	## does ols returns intercept, slope and list of predictions
	## in the time range
	def get_ols(self, data):
		Y = data
		X = range(len(data))
		X = sm.add_constant(X)
		model 			 = sm.OLS(Y,X)
		results 		 = model.fit()
		intercept, slope = results.params
		return intercept, slope, results.predict(X)

	def get_forecast(self, data):
		data_lst = []
		
		for dt in sorted(data.keys(), reverse=True):
			data_lst.append([dt, data[dt]])
		
		a = pd.DataFrame.from_records(data_lst, columns=['ds','y'])

		m = Prophet()
		m.fit(a)
		future = m.make_future_dataframe(periods=3*31)
		forecast = m.predict(future)
		records = forecast.to_dict('records')
		final = {}
		
		for row in records:
			final[str(row['ds'])[:10]] = row
		return final

	def return_current(self, current_data):
		rows = []
		rows_dict = {}
		for row in current_data:
			hour, cnt = row
			hour = int(hour)
			rows_dict[hour] = cnt

		total = 0
		for hour in range(24):
			if hour in rows_dict:
				cnt = rows_dict[hour]
			else:
				cnt = 0
		
			total += cnt
			if hour == 0:
				hour = "12 am"
			elif hour <= 13:
				hour = "%s am" % str(hour)
			else:
				hour = "%s pm" % str(hour - 12)
			rows.append({
				"hour": hour,
				"cnt": total
				})
		return rows

		# 		hours = []
		# cnts = []
		# for row in current_data:
		# 	hour, cnt = row
		# 	hours.append(hour)
		# 	cnts.append(cnt)
		# return {"hours": hours, "cnts": cnts}

	def return_data(self, orig_data):
		
		# orig_data = self.transform_data(orig_data)
		
		data = {
				"week": {
					"current_dts": 	[(self.today - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 7)],
					"prev_dts": 	[(self.today - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(7, 7*2)],
					"future_dts": 	[(self.today + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(1, 7+1)],
					"current_cnt": 	[],
					"prev_cnt": 	[],
					"data": 		[],
					"future_data":	[]
				},
				"month": {
					"current_dts": 	[(self.today - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 31)],
					"prev_dts": 	[(self.today - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(31, 31*2)],
					"future_dts": 	[(self.today + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(1, 31+1)],
					"current_cnt": 	[],
					"prev_cnt": 	[],
					"data": 		[],
					"future_data": []
				},
				"three_months": {
					"current_dts": 	[(self.today - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 31*3)],
					"prev_dts": 	[(self.today - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(31*3, 31*6)],
					"future_dts": 	[(self.today + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(1, 31*3+1)],
					"current_cnt": 	[],
					"prev_cnt": 	[],
					"data": 		[],
					"future_data":	[]
				},
				"orig_data": orig_data
		}

		forecast = self.get_forecast(orig_data)

		for timeframe in ['week', 'month', 'three_months']:
			data[timeframe]["current_dts"].sort()
			data[timeframe]["prev_dts"].sort()
			for dt in data[timeframe]["current_dts"]:
				data[timeframe]["current_cnt"].append(orig_data[dt])
			for dt in data[timeframe]["prev_dts"]:
				data[timeframe]["prev_cnt"].append(orig_data[dt])

			## get trendline
			intercept, slope, trendline  = self.get_ols(data[timeframe]["current_cnt"])
			data[timeframe]["trendline"] = list(trendline)
			data[timeframe]["trendline"] = [int(x) for x in data[timeframe]["trendline"]]			

			for i in range(len(data[timeframe]["current_cnt"])):
				row = {	
						"dt_str": 		data[timeframe]["current_dts"][i],
						"dt": 			datetime.strptime(data[timeframe]["current_dts"][i], "%Y-%m-%d").strftime("%-m/%-d"),
						"prev_dt": 		data[timeframe]["prev_dts"][i],
						"cnt": 			data[timeframe]["current_cnt"][i],
						"prev_cnt": 	data[timeframe]["prev_cnt"][i],
						"trendline":	int(trendline[i])
				}
				data[timeframe]["data"].append(row)

			try:
				data["%so%s_change" % (timeframe[0], timeframe[0])] 		= int(100.0 * sum(data[timeframe]["current_cnt"])/sum(data[timeframe]["prev_cnt"]) - 100.0)
				data["%so%s_diff" 	% (timeframe[0], timeframe[0])] 		= int(slope)
				data[timeframe]["min"] 	= int(1.15 * min(data[timeframe]["current_cnt"] + data[timeframe]["prev_cnt"]))
				data[timeframe]["max"]  = int(1.15 * min(data[timeframe]["current_cnt"] + data[timeframe]["prev_cnt"]))
			except:
				data["%so%s_change" % (timeframe[0], timeframe[0])] 		= 0
				data["%so%s_diff" 	% (timeframe[0], timeframe[0])] 		= 0
				data[timeframe]["min"] 	= 0
				data[timeframe]["max"]  = 0
		
			# get future data
			for i, dt in sorted(enumerate(data[timeframe]["future_dts"])):
				row = {	
						"dt": 			datetime.strptime(dt, "%Y-%m-%d").strftime("%-m/%-d"),
						"future_cnt":	int(forecast[dt]['yhat']),
						"error": 		[int(forecast[dt]['yhat'] - forecast[dt]['yhat_lower']), int(forecast[dt]['yhat_upper'] - forecast[dt]['yhat'])]
				}
				data[timeframe]["future_data"].append(row)
		return data


if __name__ == '__main__':
	d = Data()
	d.run_all()