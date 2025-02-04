from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, type_users_admin, type_post, users_admin
from datetime import datetime

type_manager_bp = Blueprint('type_manager', __name__)

# Route to get list of neighborhoods for classification
@type_manager_bp.route('/Data/User/Types', methods=['POST'])
@jwt_required()
def User_types():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        type_users_admin_res = type_users_admin.query.all()
        type_users_admin_res_return = [{
            'id': types.id,
            'name': types.name,
            'created_at': types.date_created.strftime('%Y-%m-%d %H:%M:%S')
        } for types in type_users_admin_res]

        return jsonify({
            'status': 'success',
            'data': {
                'types': type_users_admin_res_return
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

# Route to get list of neighborhoods for classification
@type_manager_bp.route('/Data/File/Types', methods=['POST'])
@jwt_required()
def File_types():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        type_users_admin_res = type_post.query.all()
        type_users_admin_res_return = [{
            'id': types.id,
            'name': types.name,
            'created_at': types.date_created.strftime('%Y-%m-%d %H:%M:%S')
        } for types in type_users_admin_res]

        return jsonify({
            'status': 'success',
            'data': {
                'types': type_users_admin_res_return
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500