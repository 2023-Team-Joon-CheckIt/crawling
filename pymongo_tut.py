from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import certifi
import os

ca = certifi.where()
load_dotenv()

# mongodb 연결
user_id = os.environ.get("CRAWLING_WEB_USER_ID")
user_password = os.environ.get("CRAWLING_WEB_USER_PASSWORD")
conn_str = f"mongodb+srv://{user_id}:{user_password}@book.bzk2tum.mongodb.net/?retryWrites=true&w=majority"
try:
    mongo_client = MongoClient(conn_str, tlsCAFile = ca)
    print('mongodb 연결 완료')
except Exception:
    print("Mongodb Error" + Exception)


def insert_mongo(): #파일을 읽어 mongodb에 데이터 추가
    today = datetime.now().strftime('%Y-%m-%d')
    db = mongo_client['check_it']
    collection = db[today]

    file = pd.read_csv("DB_BOOKS.csv", encoding="utf-8")
    print('csv파일 분석')
    collection.insert_many(file.to_dict('records'))
    print('mongodb에 업로드')


print('데이터 업로드를 시작합니다.......')
insert_mongo()
print('데이터 업로드 종료......')