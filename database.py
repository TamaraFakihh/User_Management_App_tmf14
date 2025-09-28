#!/usr/bin/python
import sqlite3

# this connects to a local sqlite file (creates it if not found)
def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

# this creates the users table one time
def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        );
        ''')
        conn.commit()  # actually saves the create
        print("User table created successfully")
    except:
        # if we land here, table probably exists or there is another issue
        print("User table creation failed - Maybe table already exists?")
    finally:
        conn.close()

# insert a new user (dict) and then fetch it back by id
def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # using ? placeholders to avoid sql injection
        cur.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            (user['name'], user['email'], user['phone'], user['address'], user['country'])
        )
        conn.commit()  # save the insert
        inserted_user = get_user_by_id(cur.lastrowid)  # get the exact row we just made
    except:
        # if something broke during insert, undo it
        conn.rollback()
    finally:
        conn.close()
    return inserted_user

# get all users as a list of dictionaries (not tuples)
def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row  # this makes rows behave like dicts (by column name)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        # convert each row into a normal dict so it's easy to work with
        for i in rows:
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            user["address"] = i["address"]
            user["country"] = i["country"]
            users.append(user)
    except:
        # if anything fails just return empty list (not great for prod but ok for now)
        users = []
    finally:
        conn.close()
    return users

# get exactly one user by id (returns dict)
def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        # convert row object to dictionary
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["address"] = row["address"]
        user["country"] = row["country"]
    except:
        # if no row or error -> return empty dict
        user = {}
    finally:
        conn.close()
    return user

# update the user and return the fresh version from db
def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?",
            (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"])
        )
        conn.commit()
        # return the new version from db to be sure
        updated_user = get_user_by_id(user["user_id"])
    except:
        conn.rollback()
        updated_user = {}
    finally:
        conn.close()
    return updated_user

# delete by id and return a small message dict
def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message

# run this file once to create the table (so db file shows up)
if __name__ == '__main__':
    create_db_table()
