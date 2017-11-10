# import psycopg2
import json
# from datas import datas
import boto3
from datetime import datetime, timedelta
import time
from decimal import *
import numpy as np
import statsmodels.api as sm

import pandas as pd
import numpy as np
from fbprophet import Prophet
import s3fs
import pyarrow as pa
import pyarrow.parquet as pq

import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point

class Data:

	def __init__(self):
		self.hi 	= "ben"
		base 		= datetime.today()
		self.dts 	= [(base - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 417)]
		self.today 	= datetime.today()
		# self.p 		= Postgres()
		# self.d 		= DynamoDB()

	def run_all(self):
		dataset_name = 'crimes'
		neighborhoods = gpd.read_file('geodata/neighborhoods.json')
		print neighborhoods.head()
		s3 = s3fs.S3FileSystem()
		# t1 = pa.bool_()
		# t2 = pa.float16()
		# fields = [pa.field('arrest', t1), pa.field('latitude', t2),  pa.field('latitude', t2)]
		# my_schema = pa.schema(fields)
		dataset = pq.ParquetDataset(path_or_paths='bnroths/chicago-data/crimes', filesystem=s3, validate_schema=False)
		table = dataset.read(columns=['latitude', 'longitude', 'date'])

		df = table.to_pandas()
		df['date'] = pd.to_datetime(df.date)
		df['year-month'] = df['date'].dt.strftime('%Y-%m')

		geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
		df = df.drop(['latitude', 'longitude'], axis=1)
		crs = {'init': 'epsg:4326'}
		gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
		neighborhoods_w_crime = gpd.sjoin(gdf, neighborhoods, how="inner", op='intersects')
		df = neighborhoods_w_crime.groupby(['pri_neigh', 'year-month']).agg(['count'])

		json_res = {}
		for index, row in df.iterrows():
			area, year_month = index
			val = row['count']
			if area not in json_res:
				json_res[area] = {}
			json_res[area][year_month] = val
		print json_res
		with open('../frontend/src/data/neighborhoods_%s.json' % dataset_name, 'w') as f:
			f.write(json.dumps(json_res))
		print df.head()
		

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