from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, users_admin, DaysProfitForFactor, NumberProfitForFactor



factors_price_system_bp = Blueprint('factors_price_system', __name__)


@factors_price_system_bp.route('/Factor/Days/List', methods=['GET'])
@jwt_required()
def factor_days_list():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        # Retrieve all records from DaysProfitForFactor
        days_profit_list = [{
            'id': profit.id,
            'days': profit.days,
            'profit': profit.profit,
            'created_at': profit.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for profit in DaysProfitForFactor.query.all()]

        return jsonify({
            'status': 'success',
            'data': {
                'days_profit_list': days_profit_list
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


@factors_price_system_bp.route('/Factor/Days/Create', methods=['POST'])
@jwt_required()
def factor_days_create():
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
        days = request_data.get('days')
        profit = request_data.get('profit')

        # Create a new DaysProfitForFactor record
        new_profit_record = DaysProfitForFactor(days=days, profit=profit)
        db.session.add(new_profit_record)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Record created successfully.',
            'data': {
                'id': new_profit_record.id,
                'days': new_profit_record.days,
                'profit': new_profit_record.profit,
                'created_at': new_profit_record.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


@factors_price_system_bp.route('/Factor/Days/Edit/<int:id>', methods=['PUT'])
@jwt_required()
def factor_days_edit(id):
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

        # Find the existing record by ID
        profit_record = DaysProfitForFactor.query.get(id)

        if not profit_record:
            return jsonify({
                'status': 'error',
                'message': f'Record with id {id} not found.'
            }), 404

        # Update the record
        profit_record.days = request_data.get('days', profit_record.days)
        profit_record.profit = request_data.get('profit', profit_record.profit)

        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'Record with id {id} updated successfully.',
            'data': {
                'id': profit_record.id,
                'days': profit_record.days,
                'profit': profit_record.profit,
                'created_at': profit_record.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


@factors_price_system_bp.route('/Factor/Days/Delete/<int:id>', methods=['DELETE'])
@jwt_required()
def factor_days_delete(id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        # Find the existing record by ID
        profit_record = DaysProfitForFactor.query.get(id)

        if not profit_record:
            return jsonify({
                'status': 'error',
                'message': f'Record with id {id} not found.'
            }), 404

        # Delete the record
        db.session.delete(profit_record)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'Record with id {id} deleted successfully.'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500

#--------------------------------------------------

@factors_price_system_bp.route('/Factor/Number/List', methods=['GET'])
@jwt_required()
def factor_number_list():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        # Retrieve all records from NumberProfitForFactor
        number_profit_list = [{
            'id': profit.id,
            'number_person': profit.number_person,
            'profit': profit.profit,
            'created_at': profit.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for profit in NumberProfitForFactor.query.all()]

        return jsonify({
            'status': 'success',
            'data': {
                'number_profit_list': number_profit_list
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! ：{str(e)}'
        }), 500


@factors_price_system_bp.route('/Factor/Number/Create', methods=['POST'])
@jwt_required()
def factor_number_create():
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                'status': 'error',
                'message': "شما دسترسی به این بخش ندارید !"
            }), 403

        request_data = request.get_json()

        # Create a new NumberProfitForFactor record
        new_profit_record = NumberProfitForFactor(
            number_person=request_data.get('number_person'),
            profit=request_data.get('profit')
        )

        db.session.add(new_profit_record)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Record created successfully.",
            "data": {
                "id": new_profit_record.id,
                "number_person": new_profit_record.number_person,
                "profit": new_profit_record.profit,
                "created_at": new_profit_record.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"مشکلی پیش اومده ! ：{str(e)}"
        }), 500

@factors_price_system_bp.route('/Factor/Number/Edit/<int:id>', methods=['PUT'])
@jwt_required()
def factor_number_edit(id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                "status": "error",
                "message": "شما دسترسی به این بخش ندارید !"
            }), 403

        request_data = request.get_json()

        # Find the existing record by ID
        profit_record = NumberProfitForFactor.query.get(id)

        if not profit_record:
            return jsonify({
                "status": "error",
                "message": f"Record with id {id} not found."
            }), 404

        # Update the record
        profit_record.number_person = request_data.get("number_person", profit_record.number_person)
        profit_record.profit = request_data.get("profit", profit_record.profit)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"Record with id {id} updated successfully.",
            "data": {
                "id": profit_record.id,
                "number_person": profit_record.number_person,
                "profit": profit_record.profit,
                "created_at": profit_record.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"مشکلی پیش اومده ! ：{str(e)}"
        }), 500

@factors_price_system_bp.route('/Factor/Number/Delete/<int:id>', methods=['DELETE'])
@jwt_required()
def factor_number_delete(id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']

        admin = users_admin.query.filter_by(phone=user_phone).first()

        if not admin or admin.status != 1:
            return jsonify({
                "status": "error",
                "message": "شما دسترسی به این بخش ندارید !"
            }), 403

        # Find the existing record by ID
        profit_record = NumberProfitForFactor.query.get(id)

        if not profit_record:
            return jsonify({
                "status": "error",
                "message": f"Record with id {id} not found."
            }), 404

        # Delete the record
        db.session.delete(profit_record)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"Record with id {id} deleted successfully."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"مشکلی پیش اومده ! ：{str(e)}"
        }), 500

