from routes.db import select_query, execute_query
from flask import Flask, jsonify, Blueprint, request
from flask_restful import reqparse, abort, Api, Resource

actor_api = Blueprint('actor_api', __name__)
api = Api(actor_api)

class Actor(Resource):
    def get(self, actor_id):
        try:
            actor_id = int(actor_id)
        except:
            return "Actor not found", 404

        sql = f"SELECT * FROM actor WHERE id = {actor_id}"
        results = select_query(sql)
        
        return jsonify(
            id = results[0],
            mdl_id = results[1],
            first_name = results[2],
            last_name = results[3],
            native_name = results[4],
            other_names = results[5],
            nationality = results[6],
            gender = results[7],
            birthdate = results[8],
            age = results[9],
            biography = results[10],
            picture_path = results[11]
        )
    



api.add_resource(Actor, '/actors/<actor_id>')