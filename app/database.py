import psycopg2
from psycopg2.extras import RealDictCursor
import time
from config import setting

while True:


    try:
        conn = psycopg2.connect(host=setting.database_hostname, database=setting.database_name, user=setting.database_username,
        password=setting.database_password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)