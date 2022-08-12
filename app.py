from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from resources.user import Authentication
from resources.files import UploadAadhar, UploadPan

app = Flask(__name__)

cors=CORS(app,resources={r'/api/*':{'origins':'*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xdzdamxo:4Fh_Y5nipenpeNZCSnv_3VyabOEYgPC9@tiny.db.elephantsql.com/xdzdamxo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)


from db import db
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

class App(Resource):

    # Check if server is running
    def get(self):
        return "Welcome to Antons-Flask-Backend"


auth_routes=["/api/auth/login", "/api/auth/register"]
api.add_resource(App, '/api')
api.add_resource(Authentication, *auth_routes)
api.add_resource(UploadAadhar,'/api/image/upload/aadhar')
api.add_resource(UploadPan,'/api/image/upload/pan')
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=True)