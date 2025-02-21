from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Neighborhood, db, Neighborhoods_For_Scrapper
from datetime import datetime


neighborhoods_bp = Blueprint('neighborhoods', __name__)


@neighborhoods_bp.route('/Neighborhoods/List', methods=['POST'])
@jwt_required()
def neighborhoods_list():
    try:
        request_data = request.get_json()
        name = request_data.get('name')
        date_created = request_data.get('date_created')  # Expecting a date string
        city_id = request_data.get('city_id')

        # Initialize the query
        query = Neighborhood.query

        # Check if 'name' is provided and is a valid string
        if isinstance(name, str):
            query = query.filter(Neighborhood.name.ilike(f'%{name}%'))

        # Check if 'date_created' is provided and is a valid date string
        if date_created:
            try:
                # Convert the date string to a datetime object
                date_created_obj = datetime.fromisoformat(date_created)
                query = query.filter(Neighborhood.date_created >= date_created_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

        # Check if 'city_id' is provided and is a valid integer
        if city_id is not None:
            if isinstance(city_id, int):
                query = query.filter(Neighborhood.city_id == city_id)
            else:
                return jsonify({'error': 'city_id must be an integer'}), 400

        # Execute the query
        neighborhoods = query.all()

        # Prepare and return the response
        return jsonify([{"id": n.id, "name": n.name, "city_id": n.city_id, "date_created": n.date_created} for n in neighborhoods]), 200

    except Exception as e:
        print(e)  # Log the error for debugging purposes
        return jsonify({'error': 'An error occurred while fetching neighborhoods', 'message': str(e)}), 500


# Route to edit a neighborhood
@neighborhoods_bp.route('/Neighborhoods/<int:id>', methods=['PUT'])
@jwt_required()
def edit_neighborhood(id):
    try:

        data = request.get_json()
        neighborhood = Neighborhood.query.filter_by(id=id).first()

        if not neighborhood:
            return jsonify({
                'status': 'error',
                'message': 'محله موجود نیست !'
            }), 403

        if 'name' in data:
            neighborhood.name = data['name']

        db.session.commit()
        return jsonify({"message": "محله با موفقیت تغییر یافت"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"message": f"Error {e}"}), 200

# Route to delete a neighborhood
@neighborhoods_bp.route('/Neighborhoods/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_neighborhood(id):
    neighborhood = Neighborhood.query.filter_by(id=id).first()
    if not neighborhood:
        return jsonify({
            'status': 'error',
            'message': 'محله موجود نیست !'
        }), 403
    db.session.delete(neighborhood)
    db.session.commit()

    return jsonify({"message": "محله با موفقیت حذف شد !"}), 200

@neighborhoods_bp.route('/Neighborhoods', methods=['POST'])
@jwt_required()
def add_neighborhood():
    try:
        data = request.get_json()

        # بررسی وجود نام محله در داده‌های ورودی
        if 'name' not in data or 'city_id' not in data:
            return jsonify({"message": "Name and city_id are required"}), 400

        # ایجاد یک محله جدید
        new_neighborhood = Neighborhood(
            name=data['name'],
            city_id=data['city_id'],
            date_created=datetime.now()
        )

        # اضافه کردن محله به دیتابیس
        db.session.add(new_neighborhood)
        db.session.commit()

        return jsonify({"message": "Neighborhood added successfully", "id": new_neighborhood.id}), 201
    except Exception as e:
        print(e)
        return str(e)

#------------------------------------------
#-------------- Neighborhoods_For_Scrapper
#------------------------------------------

@neighborhoods_bp.route('/Scrapper/Neighborhoods/List', methods=['POST'])
@jwt_required()
def scrapper_neighborhoods_list():
    try:
        request_data = request.get_json()
        name = request_data.get('name')
        date_created = request_data.get('date_created')  # Expecting a date string
        city_id = request_data.get('city_id')

        # Initialize the query
        query = Neighborhoods_For_Scrapper.query

        # Check if 'name' is provided and is a valid string
        if isinstance(name, str):
            query = query.filter(Neighborhoods_For_Scrapper.name.ilike(f'%{name}%'))

        # Check if 'date_created' is provided and is a valid date string
        if date_created:
            try:
                # Convert the date string to a datetime object
                date_created_obj = datetime.fromisoformat(date_created)
                query = query.filter(Neighborhoods_For_Scrapper.date_created >= date_created_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

        # Check if 'city_id' is provided and is a valid integer
        if city_id is not None:
            if isinstance(city_id, int):
                query = query.filter(Neighborhoods_For_Scrapper.city_id == city_id)
            else:
                return jsonify({'error': 'city_id must be an integer'}), 400

        # Execute the query
        neighborhoods = query.all()

        # Prepare and return the response
        return jsonify([{"id": n.id, "name_in_divar": n.name, "neighborhoods_id_in_arka": n.neighborhoods_id,
                         "city_id": n.city_id, "date_created": n.date_created} for n in
                        neighborhoods]), 200

    except Exception as e:
        print(e)  # Log the error for debugging purposes
        return jsonify({'error': 'An error occurred while fetching neighborhoods', 'message': str(e)}), 500


@neighborhoods_bp.route('/Scrapper/Neighborhoods', methods=['POST'])
@jwt_required()
def scrapper_add_neighborhood():
    try:
        data = request.get_json()

        # بررسی وجود نام محله در داده‌های ورودی
        if 'name' not in data or 'city_id' not in data or 'neighborhoods_id' not in data or 'scrapper_id' not in data:
            return jsonify({"message": "Name and city_id are required"}), 400

        # ایجاد یک محله جدید
        new_neighborhood = Neighborhoods_For_Scrapper(
            name=data['name'],
            city_id=data['city_id'],
            neighborhoods_id=data['neighborhoods_id'],
            scrapper_id=data['scrapper_id'],
            date_created=datetime.now()
        )

        # اضافه کردن محله به دیتابیس
        db.session.add(new_neighborhood)
        db.session.commit()

        return jsonify({"message": "Neighborhood added successfully", "id": new_neighborhood.id}), 201
    except Exception as e:
        print(e)
        return str(e)

@neighborhoods_bp.route('/Scrapper/Neighborhoods/<int:id>', methods=['DELETE'])
@jwt_required()
def scrapper_delete_neighborhood(id):
    neighborhood = Neighborhoods_For_Scrapper.query.filter_by(id=id).first()
    if not neighborhood:
        return jsonify({
            'status': 'error',
            'message': 'محله موجود نیست !'
        }), 403
    db.session.delete(neighborhood)
    db.session.commit()

    return jsonify({"message": "محله با موفقیت حذف شد !"}), 200