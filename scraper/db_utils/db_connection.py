import psycopg2
import psycopg2.pool
from dotenv import load_dotenv
import os
from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine

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

def get_engine():
    url = 'postgresql+psycopg2://chillywafflez:ilovekdramas1532@k-drama-tracker-db.cdoxevnwyxjg.us-west-1.rds.amazonaws.com:5432/initial_k_drama_tracker_db'
    if not database_exists(url):
        print("bruh")
    else:
        print("yippee")

    engine = create_engine(url)
    return engine