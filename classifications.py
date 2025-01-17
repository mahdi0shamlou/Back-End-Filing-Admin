from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Classification, ClassificationTypes, ClassificationNeighborhood, users_admin, Neighborhood, Types_file
from datetime import datetime


classification_bp = Blueprint('classification', __name__)
#-----------------------------------------------------
# Create and list and Delete and details of Classification
#-----------------------------------------------------
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
            'types': classification.types,
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

@classification_bp.route('/Classification/Details/<int:classification_id>', methods=['POST'])
@jwt_required()
def classification_details(classification_id):
    try:
        classification_data = (
            db.session.query(Classification)
            .filter(Classification.id == classification_id)
            .join(ClassificationNeighborhood, ClassificationNeighborhood.classifiction_id == Classification.id)
            .join(Neighborhood, Neighborhood.id == ClassificationNeighborhood.neighborhood_id)
            .join(ClassificationTypes, ClassificationTypes.classifiction_id == Classification.id)
            .join(Types_file, Types_file.id == ClassificationTypes.type)
            .add_columns(
                Classification.name.label('classification_name'),
                Neighborhood.name.label('neighborhood_name'),
                Neighborhood.id.label('neighborhood_id'),
                Types_file.id.label('type_id'),
                Types_file.name.label('type_name')
            )
            .all()
        )

        if not classification_data:
            return jsonify({"message": "Classification not found"}), 404

        # Prepare the response data
        response_data = {
            'classification_id': classification_id,
            'classification_name': classification_data[0].classification_name,
            'neighborhoods': [],
            'types': []
        }

        # Extract neighborhoods and types
        for entry in classification_data:
            neighborhood_name = entry.neighborhood_name
            type_name = entry.type_name
            neighborhood_id = entry.neighborhood_id
            type_id = entry.type_id

            if neighborhood_name and neighborhood_name not in response_data['neighborhoods']:
                response_data['neighborhoods'].append([neighborhood_name, neighborhood_id])

            if type_name and type_name not in response_data['types']:
                response_data['types'].append([type_name, type_id])

        return jsonify(response_data), 200

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
            types=request_data['types']
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

@classification_bp.route('/Classification/Edit/<int:classification_id>', methods=['PUT'])
@jwt_required()
def classification_edit(classification_id):
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
        request_data = request.get_json()
        classification.name = request_data['name']
        classification.types = request_data['types']
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'دسته بندی با موفقیت تغییر یافت!'}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


#-----------------------------------------------------
# Add and Delete Neighborhoods of Classification
#-----------------------------------------------------
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
@classification_bp.route('/Classification/Neighborhoods/<int:classification_id>/Delete', methods=['Delete'])
@jwt_required()
def classification_delete_neighborhoods(classification_id):
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
        neighborhood_id = request_data['neighborhood_id']

        query = ClassificationNeighborhood.query
        query = query.filter(ClassificationNeighborhood.classifiction_id == classification_id)
        query = query.filter(ClassificationNeighborhood.neighborhood_id == neighborhood_id)

        if not query.first():
            return jsonify({'status': 'okay', 'message': 'محله در این دسته بندی وجود ندارد !'}), 200
        else:
            db.session.delete(query.first())
            db.session.commit()
            return jsonify({'status': 'okay', 'message': 'محله از این دسته بندی حذف شد!'}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

# Route to get list of neighborhoods for classification
@classification_bp.route('/Classification/Neighborhoods/List', methods=['POST'])
@jwt_required()
def neighborhoods_list():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        neighborhoods_list_for_res = Neighborhood.query.all()
        neighborhoods_list_for_return = [{
            'id': neighborhood.id,
            'city_id': neighborhood.city_id,
            'name': neighborhood.name,
            'created_at': neighborhood.date_created.strftime('%Y-%m-%d %H:%M:%S')
        } for neighborhood in neighborhoods_list_for_res]

        return jsonify({
            'status': 'success',
            'data': {
                'neighborhood': neighborhoods_list_for_return
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


#-----------------------------------------------------
# Add and Delete Types of Classification
#-----------------------------------------------------
# Route to add neighborhoods to Type
@classification_bp.route('/Classification/Type/<int:classification_id>/Add', methods=['POST'])
@jwt_required()
def classification_add_type(classification_id):
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
        types_id = request_data['types_id']

        neighborhood = Types_file.query.filter_by(id=types_id)
        if not neighborhood.first():
            return jsonify({'status': 'error', 'message': 'نوع فایل پیدا نشد!'}), 404

        query = ClassificationTypes.query
        query = query.filter(ClassificationTypes.classifiction_id == classification_id)
        query = query.filter(ClassificationTypes.type == types_id)

        if not query.first():
            new_ClassificationTypes = ClassificationTypes(
                classifiction_id=classification_id,
                type=types_id
            )
            db.session.add(new_ClassificationTypes)
            db.session.commit()
            return jsonify({'status': 'okay', 'message': 'نوع فایل اضافه شد!'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'نوع فایل تکراری است!'}), 404

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

# Route to delete neighborhoods from Type
@classification_bp.route('/Classification/Type/<int:classification_id>/Delete', methods=['Delete'])
@jwt_required()
def classification_delete_type(classification_id):
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
        types_id = request_data['types_id']

        query = ClassificationTypes.query
        query = query.filter(ClassificationTypes.classifiction_id == classification_id)
        query = query.filter(ClassificationTypes.type == types_id)

        if not query.first():
            return jsonify({'status': 'okay', 'message': 'نوع فایل در این دسته بندی وجود ندارد !'}), 200
        else:
            db.session.delete(query.first())
            db.session.commit()
            return jsonify({'status': 'okay', 'message': 'نوع فایل از این دسته بندی حذف شد!'}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

# Route to get list of neighborhoods for classification
@classification_bp.route('/Classification/Type/List', methods=['POST'])
@jwt_required()
def Type_list():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        Types_file_list_for_res = Types_file.query.all()
        Types_file_list_for_res_return = [{
            'id': types.id,
            'name': types.name,
            'created_at': types.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for types in Types_file_list_for_res]

        return jsonify({
            'status': 'success',
            'data': {
                'types': Types_file_list_for_res_return
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500