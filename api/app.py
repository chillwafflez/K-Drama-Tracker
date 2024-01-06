from db import get_connection, get_pool
from flask import Flask, jsonify
import json

app = Flask(__name__)
pool = get_pool()

@app.get("/")
def home():
    return "Hello, world! boi"

@app.route('/drama/<drama_id>', methods=['GET'])
def get_drama(drama_id):
    try:
        drama_id = int(drama_id)
    except:
        return "Error", 404

    sql = "SELECT * FROM drama WHERE drama_id = 1;"
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchone()
    drama_details = {}
    drama_details['title'], drama_details['native_title'] = results[1], results[2]
    drama_details['synopsis'], drama_details['rating'] = results[4], float(results[5])
    drama_details['episode_count'], drama_details['mdl_id'] = results[6], results[7]
    drama_details['content_rating'], drama_details['air_dates'], drama_details['airing'] = results[8], results[9], results[10]

    pool.putconn(conn)
    return jsonify(drama_details)


if __name__ == '__main__':
    app.run(debug=True)

