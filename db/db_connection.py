import psycopg2
import psycopg2.pool
from dotenv import load_dotenv
import os

def get_connection():
    try:
        load_dotenv() 
        print("Connecting to PostgreSQL database...")

        conn = psycopg2.connect(host = os.environ.get("DB_HOST"),
                                database = os.environ.get("DB_NAME"),
                                user = os.environ.get("DB_USER"),
                                password = os.environ.get("DB_PASSWORD"))
        print(f"Successfully connected")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_pool():
    try:
        load_dotenv()
        print("Creating connection pool (min = 2, max = 3)")
        
        pool = psycopg2.pool.SimpleConnectionPool( 
            2, 3, user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD"), 
            host=os.environ.get("DB_HOST"), port='5432', database=os.environ.get("DB_NAME"))
        print(f"Successfully connected!")
        return pool
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
