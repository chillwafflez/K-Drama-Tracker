from db import get_connection, get_pool
from flask import Flask, Response
from drama import drama_api
from flask_restful import Api

app = Flask(__name__)
app.register_blueprint(drama_api)


@app.route("/", methods=['GET'])
def home():
    return Response("YIPPEE", 200)


if __name__ == '__main__':
    app.run(debug=True)

