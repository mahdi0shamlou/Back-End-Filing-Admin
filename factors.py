from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, users_admin, Factor, users, UserAccess, Users_in_Factors_Acsess, FactorAccess
from datetime import datetime


factors_bp = Blueprint('factors', __name__)
#-----------------------------------------------------
# Create and list and Delete and details of Factors
#-----------------------------------------------------
# Route to list and search Factors
@factors_bp.route('/Factor/List', methods=['POST'])
@jwt_required()
def factor_list():
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

        search_created_at = request_data.get('created_at', None)  # تاریخ ایجاد
        search_expired_at = request_data.get('expired_at', None)  # تاریخ انقضا


        # ساخت کوئری پایه
        query = Factor.query.join(users, users.id == Factor.user_id).add_columns(users)

        if search_created_at:
            created_at_date = datetime.strptime(search_created_at, '%Y-%m-%d')
            query = query.filter(Factor.created_at >= created_at_date)
        if search_expired_at:
            expired_at_date = datetime.strptime(search_expired_at, '%Y-%m-%d')
            query = query.filter(Factor.expired_at >= expired_at_date)


        # انجام pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        print(query.all()[0])

        factors_list = [{
            'id': factor.id,
            'status': factor.status,
            'type': factor.type,
            "number": factor.number,
            "price": factor.price,
            "expired_at": factor.expired_at.strftime('%Y-%m-%d %H:%M:%S'),
            'created_at': factor.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': user.id,  # Accessing user data
            'user_phone': user.phone,  # Accessing user data
            'user_name': user.name  # Accessing user data
        } for factor, user in pagination.items]

        return jsonify({
            'status': 'success',
            'data': {
                'factors_list': factors_list,
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