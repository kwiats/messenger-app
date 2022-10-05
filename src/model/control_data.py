from calendar import c
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    database="d5q3gcdmi3left",
    user='ykrewconjnhwqv',
    password='8142addde131d7fdfc06797345a86e2fd7be5c3e38fdb2063cb5248fc2e99491',
    host='ec2-52-18-116-67.eu-west-1.compute.amazonaws.com',
    port= '5432'
)

#connection.autocommit()
cursor = conn.cursor()

query = "SELECT * FROM users;"


cursor.execute(query)
lst_username = [name for name in cursor.fetchall()]
    
conn.commit()
conn.close()