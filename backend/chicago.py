# serverless deploy
# serverless invoke -f hello -l
# serverless invoke local --function hello
# pip install -t vendored/ -r requirements.txt

import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored")) 

import json
import requests
import time
import psycopg2
import pprint 
import uuid

datasets = {
    'crimes': {
        'done': True,
        'dataset_name': 'crimes_2001_to_present',
        'columns': ['id', 'date', 'latitude', 'longitude']
    },
    'graffiti_311': {
        'done': True,
        'dataset_name': '311_service_requests_graffiti_removal',
        'columns': ['service_request_number', 'creation_date', 'latitude', 'longitude']
    },
    'vacant_311': {
        'done': True,
        'dataset_name': '311_service_requests_vacant_and_abandoned_building',
        'columns': ['service_request_number', 'date_service_request_was_received', 'latitude', 'longitude']
        # any_people_using_property_homeless_childen_gangs
    },
    'alley_lights_out_311': {
        'done': False,
        'dataset_name': '311_service_requests_alley_lights_out',
        'columns': ['service_request_number', 'creation_date', 'latitude', 'longitude']
    },
    'sanitation_311': {
        'done': True,
        'dataset_name': '311_service_requests_sanitation_code_complaints',
        'columns': [None, 'creation_date', 'latitude', 'longitude']
    },
    # 'redlight_tickets': {
    #     'done': True,
    #     'dataset_name': 'chicago_redlight_tickets_csv',
    #     'columns': [None, 'issue_time', 'latitude', 'longitude'],
    # },
    'food_inspections': {
        'done': True,
        'dataset_name': 'food_inspections',
        'columns': ['inspection_id', 'inspection_date', 'latitude', 'longitude'],
    },
    'liquor_licenses': {
        'done': True,
        'dataset_name': 'business_licenses_current_liquor_and_public_places',
        'columns': ['license_id', 'license_term_start_date', 'latitude', 'longitude'],
    },
    'building_violations': {
        'done': True,
        'dataset_name': 'building_violations',
        'columns': ['id', 'violation_date', 'latitude', 'longitude']
    },
    # 'tweets': {
    #     'done': True,
    #     'dataset_name': 'tweets',
    #     'columns': ['id', 'created_at', 'lat', 'lng']
    # }
}

class Postgres():

    def __init__(self, debug=False):
        self.shapefiles = [
            # 'census_blocks',
            'community_areas',
            'congressional_districts',
            'empowerment_zones',
            'neighborhoods',
            'police_beats',
            'police_districts',
            'state_congressional_districts',
            'state_senate_districts',
            'tax_increment_financing_districts',
            'ward_precincts',
            'wards',
            'zip_codes'
            ]
        self.debug = debug
        self.conn = psycopg2.connect(dbname="uchicago", 
                                        user="bnroths", 
                                        password="sF4fLshzyzfNgEC", 
                                        host="uchicago.ctluqxmlzcvq.us-east-1.rds.amazonaws.com", 
                                        port="5432",
                                        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def insert_json_raw(self, table, json_response, check_ids=True):
        # exit(0)
       for i, row in enumerate(json_response):
            # print i, row
            query = """
            INSERT INTO datasets.%s (id, dt, lat, lng, json_data) VALUES (%%s, %%s, %%s, %%s, %%s)
            ON CONFLICT ("id")
            DO UPDATE
            SET
                "dt" = %%s,
                "lat" = %%s,
                "lng" = %%s,
                "json_data" = %%s
            """ % table
            # print query
            # exit(0)

            if datasets[table]['columns'][0]:
                row_id = str(row[datasets[table]['columns'][0]])
            else:
                row_id = str(uuid.uuid4())

            # print ids_in_table
            # print type(row_id)
            # exit(0)
            # print "insert", row_id
            self.cur.execute(query, (
                row_id, # id
                row[datasets[table]['columns'][1]], # date
                row[datasets[table]['columns'][2]], # lat
                row[datasets[table]['columns'][3]], # lng
                json.dumps(row), # everything,
                row[datasets[table]['columns'][1]], # date
                row[datasets[table]['columns'][2]], # lat
                row[datasets[table]['columns'][3]], # lng
                json.dumps(row) # everything
             ))
            # else:
            #     print "pass", row_id
            # print self.cur.query()

class Download():

    def __init__(self):
        self.name   = 'Ben'

    def download_data(self, dataset_name=None):
        url = 'http://plenar.io/v1/api/datadump?dataset_name=%s&data_type=json&obs_date__ge=2017-06-01' % datasets[dataset_name]['dataset_name']
        print url
        return requests.get(url).json()

    def transform_json(self, json):
        arr = []
        for row in json:
            arr.append(row['properties'])
        return arr

def handler(event, context):
    p = Postgres()
    d = Download()

    for table in datasets.keys():
        # p.delete_from_table(table)
        # if not datasets[table]['done']:
        print table
        res = d.download_data(table)
        # print table
        # print res
        # print [str(x) for x in res['features'][0]['properties'].keys()]
        pprint.pprint(res['features'][0]['properties'])
        # exit(0)
        new_json = d.transform_json(res['features'])
        p.insert_json_raw(table, new_json)
    

    return {"result": "GTG"}