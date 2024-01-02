import psycopg2
from dotenv import load_dotenv
import os

try:
    load_dotenv()
    
    print("Connecting to PostgreSQL database...")

    conn = psycopg2.connect(host = os.environ.get("DB_HOST"),
                            database = os.environ.get("DB_NAME"),
                            user = os.environ.get("DB_USER"),
                            password = os.environ.get("DB_PASSWORD"))
    
    cur = conn.cursor()

    # test statement
    print("PostgreSQL database version: ")
    cur.execute('SELECT * FROM drama')

    print(cur.fetchone())

    cur.close()
    conn.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
                        
