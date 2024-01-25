from db import get_connection, get_pool, select_query, select_all_query
from flask import Flask, jsonify, Blueprint
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

class Drama(Resource):
    def get(self, drama_id):
        try:
            drama_id = int(drama_id)
        except:
            return "Error", 404

        sql = f"SELECT * FROM drama WHERE drama.id = {drama_id};"
        results = select_query(sql)
        
        drama_info = {}
        drama_info['mdl_id'], drama_info['title'], drama_info['native_title'] = results[1], results[2], results[3]
        drama_info['other_names'], drama_info['rating'], drama_info['mdl_rating'] = results[4], float(results[5]), float(results[6])
        drama_info['synopsis'], drama_info['ep_count'], drama_info['duration'] = results[7], int(results[8]), int(results[9])
        drama_info['content_rating'], drama_info['country'], drama_info['air_date'] = results[10], results[11], results[12]
        drama_info['air_year'], drama_info['airing'], drama_info['cover_path'] = int(results[13]), bool(results[14]), results[15]

        # pool.putconn(conn)
        return jsonify(results)

api.add_resource(Drama, '/dramas/<drama_id>')

if __name__ == '__main__':
    app.run(debug=True)

