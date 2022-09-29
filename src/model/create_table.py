import psycopg2


conn = psycopg2.connect(
    database="d5q3gcdmi3left",
    user='ykrewconjnhwqv',
    password='8142addde131d7fdfc06797345a86e2fd7be5c3e38fdb2063cb5248fc2e99491',
    host='ec2-52-18-116-67.eu-west-1.compute.amazonaws.com',
    port= '5432'
)

cursor = conn.cursor()

query = "CREATE TABLE users(id SERIAL PRIMARY KEY,username VARCHAR NOT NULL, password VARCHAR NOT NULL, email VARCHAR NOT NULL , photo VARCHAR, friends INTEGER);"


cursor.execute(query)
    
conn.commit()
conn.close()