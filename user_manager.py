from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import users, users_admin, db
from datetime import datetime

user_manger_bp = Blueprint('user_manger', __name__)


#-----------------------------------------------------
# Route to list and search users
#-----------------------------------------------------
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

        # دریافت پارامترهای جستجو
        search_name = request_data.get('name', None)
        search_phone = request_data.get('phone', None)
        search_address = request_data.get('address', None)
        search_created_at = request_data.get('created_at', None)  # تاریخ ثبت نام
        search_email = request_data.get('email', None)
        search_type = request_data.get('type', None)
        search_status = request_data.get('status', None)


        # ساخت کوئری پایه
        query = users_admin.query

        # اضافه کردن فیلترها بر اساس پارامترهای جستجو
        if search_name:
            query = query.filter(users_admin.name.ilike(f'%{search_name}%'))

        if search_phone:
            query = query.filter(users_admin.phone.ilike(f'%{search_phone}%'))

        if search_address:
            query = query.filter(users_admin.address.ilike(f'%{search_address}%'))

        if search_email:
            query = query.filter(users_admin.email.ilike(f'%{search_email}%'))

        if search_created_at:
            try:
                created_at_date = datetime.strptime(search_created_at, '%Y-%m-%d')
                query = query.filter(users_admin.created_at >= created_at_date)
            except ValueError:
                return jsonify({'status': 'error', 'message': 'Invalid date format for created_at. Use YYYY-MM-DD.'}), 400

        if search_type is not None:  # Check for type (can be 0, 1, 2...)
            query = query.filter(users_admin.type == search_type)

        if search_status is not None:  # Check for status (0 or 1)
            query = query.filter(users_admin.status == search_status)


        # انجام pagination
        pagination = query.paginate(
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
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status': user.status,
            'type': user.type
        } for user in pagination.items]

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


@user_manger_bp.route('/UserManager/<int:user_id>', methods=['GET'])
@jwt_required()
def UserManager_Details(user_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        user = users.query.get(user_id)

        if not user:
            return jsonify({'status': 'error', 'message': 'کاربر پیدا نشد!'}), 404

        user_details = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify({'status': 'success', 'data': user_details}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


@user_manger_bp.route('/UserManager/Edit/<int:user_id>', methods=['PUT'])
@jwt_required()
def UserManager_Edit(user_id):
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

        user = users.query.get(user_id)

        if not user:
            return jsonify({'status': 'error', 'message': 'کاربر پیدا نشد!'}), 404

        # بروزرسانی اطلاعات کاربر
        user.username = request_data.get('username', user.username)
        user.name = request_data.get('name', user.name)
        user.phone = request_data.get('phone', user.phone)
        user.address = request_data.get('address', user.address)
        user.email = request_data.get('email', user.email)

        db.session.commit()

        return jsonify({'status': 'success', 'message': 'کاربر با موفقیت ویرایش شد!'}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


@user_manger_bp.route('/UserManager/Delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def UserManager_Delete(user_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        user = users.query.get(user_id)

        if not user:
            return jsonify({'status': 'error', 'message': 'کاربر پیدا نشد!'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'کاربر با موفقیت حذف شد!'}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


@user_manger_bp.route('/UserManager/Add', methods=['POST'])
@jwt_required()
def UserManager_Add():
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

        new_user = users(
            username=request_data['username'],
            password=request_data['password'],  # توجه: رمز عبور باید هش شود!
            name=request_data['name'],
            phone=request_data['phone'],
            address=request_data['address'],
            email=request_data['email']
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'کاربر جدید با موفقیت اضافه شد!'}), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

#------------------------------------
#---------- UserManger Of Admin users
#------------------------------------


@user_manger_bp.route('/UserManager/Admin/List', methods=['POST'])
@jwt_required()
def UserManager_Admin_List():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1 or admin.type != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        request_data = request.get_json()
        page = request_data.get('page', 1)
        per_page = request_data.get('perpage', 10)

        # دریافت پارامترهای جستجو
        search_name = request_data.get('name', None)
        search_phone = request_data.get('phone', None)
        search_address = request_data.get('address', None)
        search_created_at = request_data.get('created_at', None)  # تاریخ ثبت نام

        # ساخت کوئری پایه
        query = users_admin.query

        # اضافه کردن فیلترها بر اساس پارامترهای جستجو
        if search_name:
            query = query.filter(users_admin.name.ilike(f'%{search_name}%'))

        if search_phone:
            query = query.filter(users_admin.phone.ilike(f'%{search_phone}%'))

        if search_address:
            query = query.filter(users_admin.address.ilike(f'%{search_address}%'))

        if search_created_at:
            created_at_date = datetime.strptime(search_created_at, '%Y-%m-%d')
            query = query.filter(users_admin.created_at >= created_at_date)

        # انجام pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        users_list = [{
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'status': user.status,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for user in pagination.items]

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


@user_manger_bp.route('/UserManager/Admin/Edit/<int:user_id>', methods=['PUT'])
@jwt_required()
def UserManager_Admin_Edit(user_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1 or admin.type != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403


        request_data = request.get_json()

        user = users_admin.query.get(user_id)

        if not user:
            return jsonify({'status': 'error', 'message': 'کاربر پیدا نشد!'}), 404

        # بروزرسانی اطلاعات کاربر
        user.username = request_data.get('username', user.username)
        user.name = request_data.get('name', user.name)
        user.phone = request_data.get('phone', user.phone)
        user.address = request_data.get('address', user.address)
        user.email = request_data.get('email', user.email)
        user.type = request_data.get('type', user.type)
        user.status = request_data.get('status', user.status)

        db.session.commit()

        return jsonify({'status': 'success', 'message': 'کاربر با موفقیت ویرایش شد!'}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


@user_manger_bp.route('/UserManager/Admin/Delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def UserManager_Admin_Delete(user_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1 or admin.type != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        user = users_admin.query.get(user_id)

        if not user:
            return jsonify({'status': 'error', 'message': 'کاربر پیدا نشد!'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'کاربر با موفقیت حذف شد!'}), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


@user_manger_bp.route('/UserManager/Admin/Add', methods=['POST'])
@jwt_required()
def UserManager_Admin_Add():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1 or admin.type != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        request_data = request.get_json()

        new_user = users_admin(
            username=request_data['username'],
            password=request_data['password'],  # توجه: رمز عبور باید هش شود!
            name=request_data['name'],
            phone=request_data['phone'],
            address=request_data['address'],
            email=request_data['email'],
            status=request_data['status'],
            type=request_data['type']

        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'کاربر جدید با موفقیت اضافه شد!'}), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500
