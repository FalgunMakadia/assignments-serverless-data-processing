import os
from flask import Flask, json, request
from flask_cors import CORS, cross_origin
import mysql.connector
from mysql.connector.errors import IntegrityError
import datetime

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

dbConn = mysql.connector.connect(
    host="35.238.249.95",
    user="root",
    password="root",
    database="a2"
)

dbCursor = dbConn.cursor()


@app.route("/")
@cross_origin()
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)


@app.route('/register', methods=["POST"])
@cross_origin()
def register():
    user_info = request.get_json()
    login_timestamp = datetime.datetime.now()
    users_query = "INSERT INTO users (name, email, password, topic) VALUES (%s, %s, %s, %s)"
    users_query_val = (user_info["name"], user_info["email"],
                       user_info["password"], user_info["topic"])
    user_status_query = "INSERT INTO user_status (email, status, login_timestamp) VALUES (%s, %s, %s)"
    user_status_query_val = (user_info["email"], 1, login_timestamp)
    try:
        dbCursor.execute(users_query, users_query_val)
        dbCursor.execute(user_status_query, user_status_query_val)
        dbConn.commit()
        return json.jsonify({
            "data": user_info,
            "msg": "User Registration Successful!"
        })
    except IntegrityError as e:
        return json.jsonify({
            "msg": "User Registration Failed:" + e.msg
        })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
