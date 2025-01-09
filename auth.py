from flask import request, Blueprint, jsonify
import datetime
#-------------jwt tokens
from flask_jwt_extended import create_access_token
#-------------
#------------- models
from models import users_admin as Users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/Login', methods=['POST'])
def code_checker_login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    user = Users.query.filter_by(username=username).first()
    if user.password == password:
        expires = datetime.timedelta(days=2)
        access_token = create_access_token(identity={"phone": user.phone}, expires_delta=expires)
        return jsonify({"Text": "ورود شما موفقیت آمیز بود !", "access_token": access_token}), 200
    else:
        return jsonify({"Text": "کاربر ثبت نام نشده است !"}), 400
