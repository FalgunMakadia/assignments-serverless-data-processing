import os
from flask import Flask, json, request
import mysql.connector
from mysql.connector.errors import IntegrityError
from flask_cors import CORS, cross_origin
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


@app.route('/login', methods=["GET"])
@cross_origin()
def login():
    user_info = request.get_json()
    login_timestamp = datetime.datetime.now()
    query1 = "SELECT * FROM users WHERE email = %s AND password = %s"
    query_val1 = (user_info["email"],
                  user_info["password"])
    query2 = "UPDATE user_status SET status = %s, login_timestamp = %s WHERE email = %s"
    query_val2 = (1, login_timestamp, user_info["email"])

    try:
        dbCursor.execute(query1, query_val1)
        record = dbCursor.fetchone()
        if record:
            try:
                dbCursor.execute(query2, query_val2)
                dbConn.commit()
            except IntegrityError as e:
                return json.jsonify({
                    "msg": "Login Status Update Failed:" + e.msg
                })

            return json.jsonify({
                "status": "true",
                "message": "Login Successful!",
                "user_info": {"email": record[0], "name": record[1], "password": record[2], "topic": record[3]}
            })
        else:
            return json.jsonify({
                "status": "false",
                "message": "Invalid Credentials!"
            })
    except IntegrityError as e:
        return json.jsonify({
            "msg": "User Login Failed:" + e.msg
        })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
