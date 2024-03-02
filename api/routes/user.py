from routes.db import select_query, execute_query
from flask import Flask, jsonify, Blueprint, request
from flask_restful import reqparse, abort, Api, Resource

user_api = Blueprint('user_api', __name__)
api = Api(user_api)

# Trying out request parser
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='Username')
parser.add_argument('first_name', type=str, help='First name')
parser.add_argument('last_name', type=str, help='Last name')
parser.add_argument('gender', type=str, help='Gender')
parser.add_argument('biography', type=str, help='Biography')
parser.add_argument('pfp_path', type=str, help='Profile picture')

parser.add_argument('user_id', type=int, help='User ID for user_to_drama table')
parser.add_argument('drama_id', type=int, help='Drama ID for user_to_drama table')


class User(Resource):
    def get(self, user_id):
        try:
            user_id = int(user_id)
        except:
            return "Error", 404

        sql = f"select username, first_name, last_name, gender, biography, account_created, pfp_path from user_account where id = {user_id};"
        results = select_query(sql)
        user_info = {}
        user_info['username'], user_info['first_name'], user_info['last_name'] = results[0], results[1], results[2]
        user_info['gender'], user_info['biography'], user_info['account_created'] = results[3], results[4], results[5]
        user_info['pfp_path'] = results[6]

        return jsonify(user_info)
    
    def post(self):
        user_data = request.json
        columns = ""
        values = ""
        for key, value in user_data.items():
            columns += f"{key}, "
            values += f"'{value}', "
        columns = columns.strip().rstrip(',')
        values = values.strip().rstrip(',')
        sql = f"insert into user_account ({columns}) VALUES ({values})"
        print(sql)
        execute_query(sql)
        return 'User created!', 201
    
    def put(self, user_id):
        args = parser.parse_args()

        set_str = ""
        for field, new_value in args.items():
            if new_value:
                set_str += f"{field} = '{new_value}', "
        set_str = set_str.strip().rstrip(',')

        sql = f"UPDATE user_account SET {set_str} WHERE id = {user_id};"
        execute_query(sql)
    
    def delete(self, user_id):
        sql = f"DELETE FROM user_account WHERE id = {user_id}"
        execute_query(sql)

        return {'message': "Successfully deleted account"}, 204

# create a user_drama record
@user_api.route("/user_drama", methods=['POST'])
def create_user_drama_record():
    args = parser.parse_args()
    user_id = args['user_id']
    drama_id = args['drama_id']

    if user_id == None or drama_id == None:
        return "Error, need both user id and drama id!!", 404

    data = request.json
    columns = ""
    values = ""
    for key, value in data.items():
        if value and (key != 'user_id' and key != 'drama_id'):
            columns += f"{key}, "
            values += f"{value}, "
    columns = columns.strip().rstrip(',')
    values = values.strip().rstrip(',')

    sql = f"insert into user_to_drama (user_id, drama_id, {columns}) VALUES ({user_id}, {drama_id}, {values})"
    print(sql)
    execute_query(sql)

    return "User_drama record created!", 201


api.add_resource(User, '/users/<user_id>', '/users')
# api.add_resource(Dramas, '/dramas')