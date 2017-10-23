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
# import boto3
import time
import psycopg2

api_key = 'e6c38155ea644d4891091a45a8dcc0a1'
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('articles')

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

    def insert_article(self, data):
        query = """
        INSERT INTO articles.article (url, site, author, description, title, url_to_image, published_at) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT ("url")
        DO UPDATE
        SET
            site = %s,
            author = %s,
            description = %s,
            title = %s,
            url_to_image = %s,
            published_at = %s
        """ 
        
        self.cur.execute(query, (
            data['url'],
            data['site'],
            data['author'],
            data['description'],
            data['title'],
            data['urlToImage'],
            data['publishedAt'],
            data['site'],
            data['author'],
            data['description'],
            data['title'],
            data['urlToImage'],
            data['publishedAt'],
         ))

def handler(event, context):
    p = Postgres()
    r = requests.get('https://newsapi.org/v1/sources?language=en')
    t1 = time.time()
    for s in r.json()['sources']:
        url, source, name, sorts = s['url'], s['id'], s['name'], s['sortBysAvailable']
        if 'latest' in sorts:
            sortBy = 'latest'
        elif 'top' in sorts:
            sortBy = 'top'
        else:
            sortBy = 'popular'
        r = requests.get('https://newsapi.org/v1/articles?apiKey=%s&source=%s&sortBy=%s' % (api_key, source, sortBy)).json()
        for article in r['articles']:
            article['site'] = source
            # print article
            p.insert_article(article)
            # for key in article:
            #     # for dynamo
            #     if article[key] == "":
            #         article[key] = None

    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps({})
    # }
    t2 = time.time()
    res = round(t2 - t1, 2)
    return {"ok": res}