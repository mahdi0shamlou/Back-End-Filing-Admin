from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Neighborhood, db, Neighborhoods_For_Scrapper
from datetime import datetime


neighborhoods_bp = Blueprint('neighborhoods', __name__)


# Route to list and search neighborhoods
@neighborhoods_bp.route('/Neighborhoods/List', methods=['POST'])
@jwt_required()
def neighborhoods_list():
    request_data = request.get_json()
    name = request_data.get('name', 1)
    # Search neighborhoods by name
    neighborhoods = Neighborhood.query.filter(Neighborhood.name.ilike(f'%{name}%')).all()
    return jsonify([{"id": n.id, "name": n.name, "city_id": n.city_id, "date_created": n.date_created} for n in
                    neighborhoods]), 200

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
    request_data = request.get_json()
    name = request_data.get('name', 1)
    neighborhoods = Neighborhoods_For_Scrapper.query.filter(Neighborhoods_For_Scrapper.name.ilike(f'%{name}%')).all()
    return jsonify([{"id": n.id, "name_in_divar": n.name, "neighborhoods_id_in_arka": n.neighborhoods_id, "city_id": n.city_id, "date_created": n.date_created} for n in
                    neighborhoods]), 200