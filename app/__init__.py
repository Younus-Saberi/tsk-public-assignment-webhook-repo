from flask import Flask,request,jsonify
from box import Box
from flask_pymongo import PyMongo
from app.webhook.routes import webhook
from bson.json_util import dumps
from flask_cors import CORS
from datetime import datetime

# Creating our flask app
def create_app():

    app = Flask(__name__)
    CORS(app)

    try:
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
        mongo = PyMongo(app)
        print("CONNECTION SUCCESSFULL",mongo)
    except Exception as e:
        print("Expection occured",e)
    
    # registering all the blueprints
    # app.register_blueprint(webhook)

    @app.route('/',methods=["GET"])
    def hello_world():
        user = {"name":"Badal"}
        mongo.db.demo.insert_one(user)
        print(mongo)
        return "<h1>Hello World</h1>",200

    @app.route('/push', methods=['POST'])
    def add_user():
        data = request.get_json()
        obj = Box(data)

        if data is None:
            return jsonify({"error": "Invalid Json Format"}), 400

        db_data = {
            "request_id":obj.pull_request.head.sha,
            "action":obj.action,
            "author":obj.pull_request.user.login,
            "from_branch":obj.pull_request.head.ref,
            "to_branch":obj.pull_request.head.repo.default_branch,
            "timestamp":obj.pull_request.created_at
        }

        #Formating Date in UTC
        dt = datetime.strptime(obj.pull_request.created_at,'%Y-%m-%dT%H:%M:%SZ')
        formatted_dt = dt.strftime('%d %B %Y - %I:%M %p UTC')

        #Format: {author} pushed to {to_branch} on {timestamp}
        #Sample: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC
        msg = f'{obj.pull_request.user.login} pushed to {obj.pull_request.head.repo.default_branch} on {formatted_dt}'
        mongo.db.demo.insert_one({'message':msg})

        return jsonify({'message': 'Info added successfully'}), 201

    @app.route('/get_requests',methods=["GET"])
    def get_requests():
        try:
            req = mongo.db.demo.find().sort([('_id',-1)]).limit(1)
            return dumps(req),200
        except Exception as e:
            print("Some Error Occurred",e)
            return jsonify({"error":str(e)}),500

    return app
