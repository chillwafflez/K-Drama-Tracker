from routes.db import select_query, select_all_query
from flask import Flask, jsonify, Blueprint, request
from flask_restful import Api, Resource

drama_api = Blueprint('drama_api', __name__)
api = Api(drama_api)

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

        return jsonify(drama_info)
    
class Dramas(Resource):
    def get(self):
        sql = "SELECT * FROM drama;"
        results = select_all_query(sql)

        return jsonify(results)

# Search dramas by name
@drama_api.route("/dramas/search", methods=['GET'])
def search_dramas():
    name = request.args.get('name')
    if name == None:
        return "Error", 404
    
    sql = f"SELECT id, title, native_title, rating, synopsis, episode_count, country, air_year FROM drama WHERE title ILIKE '%{name}%';"
    results = select_all_query(sql)

    print(len(results))
    return jsonify(results)


# ---- Genres, Tags, Networks ---- #

# Getting all genres for a drama
@drama_api.route("/dramas/<drama_id>/genres", methods=['GET'])
def get_drama_genres(drama_id):
    sql = f"SELECT genre.id, genre_name FROM genre JOIN drama_genre ON drama_genre.genre_id = genre.id JOIN drama ON drama_genre.drama_id = drama.id WHERE drama.id = {drama_id};"
    results = select_all_query(sql)
    return jsonify(results)

# Getting all tags for a drama
@drama_api.route("/dramas/<drama_id>/tags", methods=['GET'])
def get_drama_tags(drama_id):
    sql = f"SELECT tag.id, tag_name FROM tag JOIN drama_tag ON drama_tag.tag_id = tag.id JOIN drama ON drama_tag.drama_id = drama.id WHERE drama.id = {drama_id};"
    results = select_all_query(sql)
    return jsonify(results)

# Getting all networks for a drama
@drama_api.route("/dramas/<drama_id>/networks", methods=['GET'])
def get_drama_networks(drama_id):
    sql = f"SELECT network.id, network_name FROM network JOIN drama_network ON drama_network.network_id = network.id JOIN drama ON drama_network.drama_id = drama.id WHERE drama.id = {drama_id};"
    results = select_all_query(sql)
    return jsonify(results)

# Getting all dramas of a specific genre
@drama_api.route("/genres/<genre_id>", methods=['GET'])
def get_genre_dramas(genre_id):
    sql = f"SELECT drama.id, title, native_title, other_names, rating, cover_path FROM drama JOIN drama_genre ON drama_genre.drama_id = drama.id JOIN genre ON drama_genre.genre_id = genre.id WHERE genre.id = {genre_id};"
    results = select_all_query(sql)
    return jsonify(results)

# Getting all dramas of a specific tag
@drama_api.route("/tags/<tag_id>", methods=['GET'])
def get_tag_dramas(tag_id):
    sql = f"SELECT drama.id, title, native_title, other_names, rating, cover_path FROM drama JOIN drama_tag ON drama_tag.drama_id = drama.id JOIN tag ON drama_tag.tag_id = tag.id WHERE tag.id = {tag_id};"
    results = select_all_query(sql)
    return jsonify(results)

# Getting all dramas of a specific network
@drama_api.route("/networks/<network_id>", methods=['GET'])
def get_network_dramas(network_id):
    sql = f"SELECT drama.id, title, native_title, other_names, rating, cover_path FROM drama JOIN drama_network ON drama_network.drama_id = drama.id JOIN tag ON drama_network.tag_id = network.id WHERE network.id = {network_id};"
    results = select_all_query(sql)
    return jsonify(results)

api.add_resource(Drama, '/dramas/<drama_id>')
api.add_resource(Dramas, '/dramas')