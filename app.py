from flask import Flask, request
import os
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from resources.user import Authentication
from resources.upload import UploadAadhar, UploadPan
from resources.details import GetDetails
from resources.process import ProcessAadhar, ProcessPan
from resources.college import CollegeDetails
from resources.verification import Verification
from dotenv import load_dotenv

app = Flask(__name__)

cors=CORS(app,resources={r'/api/*':{'origins':'*'}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("PG_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response

from db import db
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

class App(Resource):

    # Check if server is running
    def get(self):
        return "Welcome to Antons-Flask-Backend"


auth_routes=["/api/auth/login", "/api/auth/register","/api/auth/profile", "/api/auth/verify"]
details_routes=["/api/details/admin","/api/details/super"]
verification_routes=["/api/verify/admin","/api/verify/super"]

api.add_resource(App, '/api')
api.add_resource(Authentication, *auth_routes)
api.add_resource(UploadAadhar,'/api/image/upload/aadhar')
api.add_resource(UploadPan,'/api/image/upload/pan')
api.add_resource(ProcessAadhar,'/api/image/process/aadhar')
api.add_resource(ProcessPan,'/api/image/process/pan')
api.add_resource(GetDetails,*details_routes)
api.add_resource(CollegeDetails,'/api/college')
api.add_resource(Verification,*verification_routes)

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)