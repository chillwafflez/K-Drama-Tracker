import psycopg2
from flask import Flask

conn = psycopg2.connect(database = "k_drama_data_TEST")


app = Flask(__name__)

@app.get("/")
def home():
    return "Hello, world!"