from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import configparser
from flask import jsonify
from models import db
from cache import cache
#-------------------------
from auth import auth_bp
from user_manager import user_manger_bp
from neighborhoods import neighborhoods_bp
from classifications import classification_bp
from cluster import cluster_bp
from factors import factors_bp
from files import files_bp
from factor_price_data import factors_price_system_bp
from Data_Select import type_manager_bp
from notes import notes_bp


config = configparser.ConfigParser()
config.read('core/db_config.ini')

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aas;ld98y2e123+@*(*^&(^*!*'
app.config['JWT_SECRET_KEY'] = 'aaASD%^&8y2e123+@*(*^&(^*!*'
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Use cookies for JWT tokens
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Enable CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config["mysql"]["user"]}:{config["mysql"]["password"]}@{config["mysql"]["host"]}/{config["mysql"]["database"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_size": 10,             # Pool size of 10 connections
    "max_overflow": 20,          # Allow up to 20 additional connections
    "pool_timeout": 20,          # Wait up to 20 seconds before timeout
    "pool_recycle": 1800         # Recycle connections every 1800 seconds (30 minutes)
}

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*", "allow_headers": ["Authorization", "Content-Type"], "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"]}})

db.init_app(app)
jwt = JWTManager(app)


cache.init_app(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 0,
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})


app.register_blueprint(auth_bp)
app.register_blueprint(user_manger_bp)
app.register_blueprint(neighborhoods_bp)
app.register_blueprint(classification_bp)
app.register_blueprint(cluster_bp)
app.register_blueprint(factors_bp)
app.register_blueprint(files_bp)
app.register_blueprint(factors_price_system_bp)
app.register_blueprint(type_manager_bp)
app.register_blueprint(notes_bp)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 401,
        'sub_status': 'توکن منقضی شده است !',
        'message': 'توکن منقضی شده است !'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'status': 402,
        'sub_status': 'توکن ارسال شده مشکل دارد !',
        'message': 'توکن ارسال شده مشکل دارد !'
    }), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({
        'status': 400,
        'sub_status': 'توکن ارسال نشده است !',
        'message': 'توکن ارسال نشده است !'
    }), 401


@app.errorhandler(404)
def not_found_error(error):
    # You can render a custom HTML template for the 404 error
    return 404

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    # This is also a place to clean up any resources if needed
    return 500



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # Or specify your frontend domain here
    response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE, PATCH')
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create SQL tables for our data models
    app.run(debug=True, port=1000)
