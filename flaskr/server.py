#!/usr/bin/env python
import os
import uuid

from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from pymongo import MongoClient
from configparser import ConfigParser
from datetime import datetime, timedelta
import base58
import os

app = Flask(__name__)

client = MongoClient("mongo:27017")

database = "tinyurl_database"
tinyurl_mapping = "tinyurl_mapping_collection"
user = "user_collection"

db = client[database]
mapping_collection = db[tinyurl_mapping]
user_collection = db[user]

config_path_from_root = "./flaskr/config.ini"
config_path = "config.ini"
config = ConfigParser()
config.read(config_path)

@app.route('/')
def todo():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return "Hello from the MongoDB client!\n"

@app.route("/create", methods=["POST"])
def create_url():
    
    def generate_tiny_url(original_url):
        host = config["WEB"]["host"] 
        base58_encoded_url = base58.b58encode_check(original_url.encode())
        return host + "/" + base58_encoded_url.decode("UTF-8")

    account_id = request.args.get("account_id")
    original_url = request.args.get("original_url")
    hours = int(request.args.get("hours"))
    exp_time_delta = timedelta(hours=hours)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    exp_dt_string = (now + exp_time_delta).strftime("%d/%m/%Y %H:%M:%S")

    tiny_url = generate_tiny_url(original_url)
    
    document = {
        "id": str(uuid.uuid4()),
        "original_url": original_url,
        "tiny_url": tiny_url,
        "create_time": dt_string,
        "modify_time": dt_string,
        "expire_time": exp_dt_string,
        "owner_id": account_id,
        "status": "active"
    }
    
    inserted_id = mapping_collection.insert_one(document).inserted_id
    
    print("inserted id per url mapping is " + str(inserted_id))
    return Response(tiny_url, mimetype="text/plain", status=200)

@app.route("/read")
def read_url():
    account_id = request.args.get("account_id")
    tiny_url = request.args.get("tiny_url")
    document = mapping_collection.find_one({"tiny_url": tiny_url, "owner_id": account_id})
    
    print("document: " + str(document))
    original_url = document["original_url"]
    return redirect(original_url, 302)

@app.route("/signup", methods=["POST"])
def sign_up():
    name = request.json.get("name")
    username = request.json.get("username")
    password = request.json.get("password")
    
    document = user_collection.find_one({"username": username, "password": password})
    if document:
        return Response("user exists. not allowed", mimetype="text/plain", status=400)
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    document = {
        "id": str(uuid.uuid4()),
        "name": name,
        "username": username,
        "password": password,
        "create_time": dt_string,
        "modify_time": dt_string
    }
    inserted_id = user_collection.insert_one(document).inserted_id
    
    print("inserted id per user is " + str(inserted_id))
    return Response("success", mimetype="text/plain", status=200)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    document = user_collection.find_one({"username": username, "password": password})
    
    if document:
        print("user " + str(document['name']) + " successfully logged in")
        return Response("success", mimetype="text/plain", status=200)
    return Response("user not exist", mimetype="text/plain", status=403)


@app.route("/update")
def update_url(account_id, tiny_url, things_to_update):
    pass

@app.route("/delete")
def delete_url(account_id, tiny_url):
    pass

if __name__ == "__main__":
    print("Starting Tiny URL app")
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)