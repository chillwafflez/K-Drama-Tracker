from db import select_query, select_all_query, execute_query
from flask import Flask, jsonify, Blueprint, request
from flask_restful import reqparse, abort, Api, Resource

review_api = Blueprint('review_api', __name__)
api = Api(review_api)

class Review(Resource):
    def get(self, review_id):
        try:
            review_id = int(review_id)
        except:
            return "Error", 404

        sql = f"SELECT * FROM review WHERE id = {review_id};"
        results = select_query(sql)

        return jsonify(
            id = results[0],
            user_id = results[1],
            drama_id = results[2],
            review = results[3],
            summary = results[4],
            score = results[5])
    
    def delete(self, review_id):
        try:
            review_id = int(review_id)
        except:
            return "Error", 404

        sql = f"DELTE FROM review WHERE id = {review_id};"
        execute_query(sql)

        return {'message': "Successfully deleted review"}, 204


# Getting all reviews of a user
@review_api.route("/users/<user_id>/reviews", methods=['GET'])
def get_user_reviews(user_id):
    sql = f"SELECT review.id, drama_id, review, summary, score FROM review JOIN user_account ON review.user_id = user_account.id WHERE user_account.id = {user_id};"
    results = select_all_query(sql)
    response = []
    for review in results:
        review_response = {}
        review_response['id'] = review[0]
        review_response['drama_id'] = review[1]
        review_response['review'] = review[2]
        review_response['summary'] = review[3]
        review_response['score'] = float(review[4])
        response.append(review_response)

    return jsonify(response)

# Getting all reviews of a drama
@review_api.route("/dramas/<drama_id>/reviews", methods=['GET'])
def get_drama_reviews(drama_id):
    sql = f"SELECT review.id, user_id, review, summary, score FROM review JOIN drama ON review.drama_id = drama.id WHERE drama.id = {drama_id};"
    results = select_all_query(sql)
    response = []
    for review in results:
        review_response = {}
        review_response['id'] = review[0]
        review_response['user_id'] = review[1]
        review_response['review'] = review[2]
        review_response['summary'] = review[3]
        review_response['score'] = float(review[4])
        response.append(review_response)

    return jsonify(response)

api.add_resource(Review, '/reviews/<review_id>')