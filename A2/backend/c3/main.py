import os
from flask import Flask, json, request
import mysql.connector
from mysql.connector.errors import IntegrityError
from flask_cors import CORS, cross_origin

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


@app.route("/dashboard", methods=["GET"])
@cross_origin()
def dashboard():
    query = "SELECT * FROM user_status WHERE status = %s"
    query_val = (1,)
    try:
        dbCursor.execute(query, query_val)
        result = dbCursor.fetchall()
        print("Result")
        print(result)
        return json.jsonify({
            "status": "true",
            "message": "Active User List Success!",
            "active_users": result
        })
    except IntegrityError as err:
        return json.jsonify({
            "status": "false",
            "message": err.msg,
        })


@app.route("/logout", methods=["GET"])
@cross_origin()
def logout():
    user_info = request.get_json()
    query = "UPDATE user_status SET status = %s WHERE email = %s"
    query_val = (0, user_info["email"])

    try:
        dbCursor.execute(query, query_val)
        dbConn.commit()
        return json.jsonify({
            "msg": "Logout Successful!",
        })
    except IntegrityError as e:
        return json.jsonify({
            "msg": "User Logout Failed:" + e.msg
        })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
