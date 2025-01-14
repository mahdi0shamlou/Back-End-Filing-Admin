from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Classification, ClassificationTypes, ClassificationNeighborhood, users_admin, Neighborhood
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
@classification_bp.route('/Classification/Create', methods=['POST'])
@jwt_required()
def classification_create():
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

        new_user = Classification(
            name=request_data['name'],
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'دسته بندیس جدید با موفقیت اضافه شد!'}), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

# Route to delete classification
@classification_bp.route('/Classification/Delete/<int:classification_id>', methods=['Delete'])
@jwt_required()
def classification_delete(classification_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        classification = Classification.query.get(classification_id)

        if not classification:
            return jsonify({'status': 'error', 'message': 'دسته بندی پیدا نشد!'}), 404

        db.session.delete(classification)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'دسته بندی با موفقیت حذف شد!'}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

# Route to add neighborhoods to classification
@classification_bp.route('/Classification/Neighborhoods/<int:classification_id>/Add', methods=['POST'])
@jwt_required()
def classification_add_neighborhoods(classification_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403
        classification = Classification.query.filter_by(id=classification_id)
        if not classification.first():
            return jsonify({'status': 'error', 'message': 'دسته بندی پیدا نشد!'}), 404

        request_data = request.get_json()
        neighborhood_id = request_data['neighborhood_id']

        neighborhood = Neighborhood.query.filter_by(id=neighborhood_id)
        if not neighborhood.first():
            return jsonify({'status': 'error', 'message': 'محله پیدا نشد!'}), 404

        query = ClassificationNeighborhood.query
        query = query.filter(ClassificationNeighborhood.classifiction_id==classification_id)
        query = query.filter(ClassificationNeighborhood.neighborhood_id==neighborhood_id)

        if not query.first():
            new_ClassificationNeighborhood = ClassificationNeighborhood(
                classifiction_id=classification_id,
                neighborhood_id=neighborhood_id
            )
            db.session.add(new_ClassificationNeighborhood)
            db.session.commit()
            return jsonify({'status': 'okay', 'message': 'محله اضافه شد!'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'محله اضافه شده بوده است!'}), 404

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


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