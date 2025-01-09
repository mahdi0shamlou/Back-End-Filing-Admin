from flask import request, Blueprint, jsonify
#-------------jwt tokens
from flask_jwt_extended import jwt_required, get_jwt_identity
#-------------
#------------- models
from models import users, users_admin, db


user_manger_bp = Blueprint('user_manger', __name__)


@user_manger_bp.route('/UserManager/List', methods=['POST'])
@jwt_required()
def UserManager_List():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        request_data = request.get_json()
        page = request_data.get('page', 1)
        per_page = request_data.get('perpage', 10)

        pagination = users.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        users_list = [{
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for user in pagination.items]
        print(users_list)
        return jsonify({
            'status': 'success',
            'data': {
                'users': users_list,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }
        }), 200


    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


