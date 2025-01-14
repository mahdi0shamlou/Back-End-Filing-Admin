from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Classifictions_FOR_Factors, users_admin, PER_Classifictions_FOR_Factors, Classification
from datetime import datetime


cluster_bp = Blueprint('cluster', __name__)
#-----------------------------------------------------
# Create and list and Delete and details of Cluster
#-----------------------------------------------------
# Route to list and search Cluster
@cluster_bp.route('/Cluster/List', methods=['POST'])
@jwt_required()
def cluster_list():
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
        query = Classifictions_FOR_Factors.query

        # اضافه کردن فیلترها بر اساس پارامترهای جستجو
        if search_name:
            query = query.filter(Classifictions_FOR_Factors.name.ilike(f'%{search_name}%'))

        if search_created_at:
            created_at_date = datetime.strptime(search_created_at, '%Y-%m-%d')
            query = query.filter(Classifictions_FOR_Factors.created_at >= created_at_date)

        # انجام pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        cluster_list = [{
            'id': cluster.id,
            'name': cluster.name,
            'price': cluster.price,
            'created_at': cluster.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for cluster in pagination.items]

        return jsonify({
            'status': 'success',
            'data': {
                'cluster_list': cluster_list,
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

# Route to create cluster
@cluster_bp.route('/Cluster/Create', methods=['POST'])
@jwt_required()
def cluster_create():
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

        new_user = Classifictions_FOR_Factors(
            name=request_data['name'],
            price=request_data['price']
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'طبقه بندی جدید با موفقیت اضافه شد!'}), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

# Route to delete cluster
@cluster_bp.route('/Cluster/Delete/<int:cluster_id>', methods=['Delete'])
@jwt_required()
def cluster_delete(cluster_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        cluster = Classifictions_FOR_Factors.query.get(cluster_id)

        if not cluster:
            return jsonify({'status': 'error', 'message': 'طبقه بندی پیدا نشد!'}), 404

        db.session.delete(cluster)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'طبقه بندی با موفقیت حذف شد!'}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

# Route to details cluster
@cluster_bp.route('/Cluster/Details/<int:cluster_id>', methods=['POST'])
@jwt_required()
def cluster_details(cluster_id):
    try:
        cluster_data = (
            db.session.query(Classifictions_FOR_Factors)
            .filter(Classifictions_FOR_Factors.id == cluster_id)
            .join(PER_Classifictions_FOR_Factors, PER_Classifictions_FOR_Factors.Classifictions_FOR_Factors_id_created == Classifictions_FOR_Factors.id)
            .join(Classification, Classification.id == PER_Classifictions_FOR_Factors.Classifictions_id_created)
            .add_columns(
                Classification.name.label('classification_name'),
                Classification.id.label('classification_id'),
                Classifictions_FOR_Factors.name.label('cluster_name'),
                Classifictions_FOR_Factors.price.label('cluster_price'),
            )
            .all()
        )

        if not cluster_data:
            return jsonify({"message": "cluster not found"}), 404

        # Prepare the response data
        response_data = {
            'cluster': cluster_id,
            'cluster_name': cluster_data[0].cluster_name,
            'cluster_price': cluster_data[0].cluster_price,
            'classifications': []
        }

        # Extract neighborhoods and types
        for entry in cluster_data:
            classification_name = entry.classification_name
            classification_id = entry.classification_id
            if classification_name and classification_name not in response_data['classifications']:
                response_data['classifications'].append([classification_name, classification_id])

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500