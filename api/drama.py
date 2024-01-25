from db import get_connection, get_pool, select_query, select_all_query
from flask import Flask, jsonify, Blueprint
from flask_restful import reqparse, abort, Api, Resource

drama_api = Blueprint('drama_api', __name__)
api = Api(drama_api)

# pool = get_pool()

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
        drama_info['other_names'], drama_info['rating'], drama_info['mdl_rating'] = results[4], results[5], results[6]
        drama_info['synopsis'], drama_info['ep_count'], drama_info['duration'] = results[7], results[8], results[9]
        drama_info['content_rating'], drama_info['country'], drama_info['air_date'] = results[10], results[11], results[12]
        drama_info['air_year'], drama_info['airing'], drama_info['cover_path'] = results[13], results[14], results[15]

        float(drama_info['rating']) if drama_info['rating'] else drama_info['rating']
        float(drama_info['mdl_rating']) if drama_info['mdl_rating'] else drama_info['mdl_rating']
        int(drama_info['ep_count']) if drama_info['ep_count'] else drama_info['ep_count']
        int(drama_info['duration']) if drama_info['duration'] else drama_info['duration']
        int(drama_info['air_year']) if  drama_info['air_year'] else  drama_info['air_year']
        bool(drama_info['airing']) if  drama_info['airing'] else  drama_info['airing']

        # pool.putconn(conn)
        return jsonify(drama_info)
    
# class Dramas(Resource):
#     def get():
#         sql = "SELECT * FROM drama;"
#         results = select_all_query(sql)

#         return jsonify(results)

# Getting dramas by genres, tags, or networks
@drama_api.route("/dramas", methods=['GET'])
def get():
    sql = "SELECT * FROM drama;"
    results = select_all_query(sql)

    return jsonify(results)

api.add_resource(Drama, '/dramas/<drama_id>')
# api.add_resource(Dramas, '/dramas')