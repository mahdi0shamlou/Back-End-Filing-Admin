from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Classification, ClassificationTypes, ClassificationNeighborhood, users_admin
from datetime import datetime


classification_bp = Blueprint('classification', __name__)


# Route to list and search classification
@classification_bp.route('/Classification/List', methods=['POST'])
@jwt_required()
def classification_list():
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

        # دریافت پارامترهای جستجو
        search_name = request_data.get('name', None)
        search_created_at = request_data.get('created_at', None)  # تاریخ ثبت نام

        # ساخت کوئری پایه
        query = Classification.query

        # اضافه کردن فیلترها بر اساس پارامترهای جستجو
        if search_name:
            query = query.filter(Classification.name.ilike(f'%{search_name}%'))

        if search_created_at:
            created_at_date = datetime.strptime(search_created_at, '%Y-%m-%d')
            query = query.filter(Classification.created_at >= created_at_date)

        # انجام pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        classification_list = [{
            'id': classification.id,
            'name': classification.name,
            'created_at': classification.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for classification in pagination.items]

        return jsonify({
            'status': 'success',
            'data': {
                'users': classification_list,
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



# Route to create classification
@classification_bp.route('/Classification/Add', methods=['POST'])
@jwt_required()
def classification_create():
    pass

# Route to delete classification
@classification_bp.route('/Classification/Delete', methods=['Delete'])
@jwt_required()
def classification_delete():
    pass

# Route to add neighborhoods to classification
@classification_bp.route('/Classification/Neighborhoods/Add', methods=['POST'])
@jwt_required()
def classification_add_neighborhoods():
    pass

# Route to delete neighborhoods from classification
@classification_bp.route('/Classification/Neighborhoods/Delete', methods=['Delete'])
@jwt_required()
def classification_delete_neighborhoods():
    pass


# Route to add neighborhoods to Type
@classification_bp.route('/Classification/Type/Add', methods=['POST'])
@jwt_required()
def classification_add_type():
    pass

# Route to delete neighborhoods from Type
@classification_bp.route('/Classification/Type/Delete', methods=['Delete'])
@jwt_required()
def classification_delete_type():
    pass