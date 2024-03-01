from flask import Flask, Response
from drama import drama_api
from user import user_api
from actor import actor_api
from review import review_api
from flask_restful import Api

app = Flask(__name__)
app.register_blueprint(drama_api)
app.register_blueprint(user_api)
app.register_blueprint(actor_api)
app.register_blueprint(review_api)


@app.route("/", methods=['GET'])
def home():
    return Response("home index", 200)


if __name__ == '__main__':
    app.run(debug=True)