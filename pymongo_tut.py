from pymongo import MongoClient
from pymysql import connect
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

def insert_mysql():
        # mysql 연결
        try:
            mysql_con = connect(
                host="127.0.0.1",
                user="root",
                password="0000",
                database="checkit"
            )
            print('mysql 연결 완료')
        except Exception:
            print("Mysql Error" + Exception)
        
        # today = datetime.now().strftime('%Y-%m-%d')
        mongo_db = mongo_client['check_it']
        collection = mongo_db['2023-03-11']

        fruits = collection.find()
        print('mongodb에서 값 가져오기')    
        mysql_cursor = mysql_con.cursor()

        for data in fruits:
            title = data['title']
            author = data['author']
            publisher = data['publisher']
            cover_image_url = data['img_url']
            pages = data['pages']
            width = data['width']
            thickness = data['thickness']
            category = data['category']

            sql = "UPDATE fruit SET price = %s WHERE name = %s"
            sql = "INSERT INTO books (title, author, publisher, cover_image_url, pages, width, thickness, category) values(%s, %s, %s, %s, %s, %s, %s, %s)" 
            injection = (str(title),str(author),str(publisher),str(cover_image_url),str(pages),str(width),str(thickness),str(category))
            mysql_cursor.execute(sql,injection)
        print('책 내용 입력')
        mysql_con.commit()
        print('mysql에 저장')
        
        mysql_cursor.close()
        mysql_con.close()


print('데이터 업로드를 시작합니다.......')
# insert_mongo()
insert_mysql()
print('데이터 업로드 종료......')