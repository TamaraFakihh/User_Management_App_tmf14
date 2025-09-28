from flask import Flask, request, jsonify   # added to top of file
from flask_cors import CORS                 # added to top of file

# pulling in my db helpers from the previous part
from database import (
    get_users,
    get_user_by_id,
    insert_user,
    update_user,
    delete_user,
    create_db_table
)

app = Flask(__name__)
# allow any origin for now (simple lab setup)
CORS(app, resources={r"/*": {"origins": "*"}})

# make sure table exists before serving (just being safe)
create_db_table()

# GET /api/users  -> list all
@app.route('/api/users', methods=['GET'])
def api_get_users():
    # just return whatever db gives me as json
    return jsonify(get_users())

# GET /api/users/<user_id> -> one user
@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    # casting to int since my db layer expects an int id
    return jsonify(get_user_by_id(int(user_id)))

# POST /api/users/add -> create new
@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    # body is json with name,email,phone,address,country
    user = request.get_json()
    return jsonify(insert_user(user))

# PUT /api/users/update -> update existing (expects user_id in body)
@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

# DELETE /api/users/delete/<user_id>
@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user_route(user_id):
    return jsonify(delete_user(int(user_id)))

if __name__ == "__main__":
    # app.debug = True
    # app.run(debug=True)
    app.run()   # run app (default: 127.0.0.1:5000)
