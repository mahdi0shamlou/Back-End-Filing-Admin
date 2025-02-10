from flask import request, Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required
from models import db, Posts, Neighborhood, Types_file, Cities, Classification
from sqlalchemy import or_
import json



files_bp = Blueprint('files', __name__)
#-----------------------------------------------------
# Create and list and Delete and details of Cluster
#-----------------------------------------------------
# Route to list all files
@files_bp.route('/Files/List', methods=['POST'])
@jwt_required()
def files_list():
    try:

        try:
            request_data = request.get_json()
            price_from = request_data.get('price_from', None)
            price_to = request_data.get('price_to', None)
            price_from_two = request_data.get('price_from_2', None)
            price_to_two = request_data.get('price_to_2', None)
            meter_from = request_data.get('meter_from', None)
            meter_to = request_data.get('meter_to', None)
            page = request_data.get('page', 1)
            otagh = request_data.get('otagh', None)
            make_from = request_data.get('make_from')
            make_to = request_data.get('make_two')
            desck = request_data.get('desck', None)
            status = request_data.get('status', None)
            allowed_mahals = request_data.get('mahal', [])
            allowed_type_ids = request_data.get('types', [])

            query = Posts.query
            if status:
                query = query.filter(Posts.status == status)

            if allowed_mahals:
                query = query.filter(Posts.mahal.in_(allowed_mahals))

            if allowed_type_ids:
                query = query.filter(Posts.type.in_(allowed_type_ids))

            if price_from is not None and price_to is not None:
                query = query.filter(Posts.price.between(price_from, price_to))
            elif price_from is not None:
                query = query.filter(Posts.price >= price_from)
            elif price_to is not None:
                query = query.filter(Posts.price <= price_to)

            if price_from_two is not None and price_to_two is not None:
                query = query.filter(Posts.price_two.between(price_from_two, price_to_two))
            elif price_from_two is not None:
                query = query.filter(Posts.price_two >= price_from_two)
            elif price_to_two is not None:
                query = query.filter(Posts.price_two <= price_to_two)

            if meter_from is not None and meter_to is not None:
                query = query.filter(Posts.meter.between(meter_from, meter_to))
            elif meter_from is not None:
                query = query.filter(Posts.meter >= meter_from)
            elif meter_to is not None:
                query = query.filter(Posts.meter <= meter_to)

            if otagh is not None:
                if otagh != -1:
                    query = query.filter(Posts.Otagh == otagh)

            if make_from is not None and make_to is not None:
                query = query.filter(Posts.Make_years.between(make_from, make_to))
            elif make_from is not None:
                query = query.filter(Posts.Make_years >= make_from)
            elif make_to is not None:
                query = query.filter(Posts.Make_years <= make_to)

            if 'parking' in request_data:
                query = query.filter(Posts.PARKING == True)

            if 'cabinet' in request_data:
                query = query.filter(Posts.CABINET == True)

            if 'elevator' in request_data:
                query = query.filter(Posts.ELEVATOR == True)

            if desck is not None:
                query = query.filter(or_(
                    Posts.desck.ilike(f'%{desck}%'),
                    Posts.title.ilike(f'%{desck}%')
                ))

            per_page = 12

            posts_pagination = query.order_by(Posts.id.desc()).paginate(page=page, per_page=per_page,
                                                                        error_out=False)

            posts = posts_pagination.items

            # Build a list of post details to send in the response
            posts_list = [{
                'id': query.id,
                'is_active': query.is_active,
                'title': query.title,
                'Images': query.Images,
                'city': query.city_text,
                'type': query.type_text,
                '_type': str(query.type)[0],
                'price': query.price,
                'price_two': query.price_two,
                'PARKING': query.PARKING,
                'CABINET': query.CABINET,
                'ELEVATOR': query.ELEVATOR,
                'BALCONY': query.BALCONY,
                'Otagh': query.Otagh,
                'Make_years': query.Make_years,
                'phone': query.number,
                'mahal': query.mahal_text,
                'meter': query.meter,
                'token': query.token,
                'desck': query.desck,
                'details': query.details,
                'floor': query.floor,
                'dwelling_units_per_floor': query.dwelling_units_per_floor,
                'dwelling_unit_floor': query.dwelling_unit_floor,
                'wc': query.wc,
                'floor_type': query.floor_type,
                'water_provider': query.water_provider,
                'cool': query.cool,
                'heat': query.heat,
                '_map': True if query.map else False,
                'building_directions': query.building_directions,
                'date_created_persian': query.date_created_persian,
                'date_created': query.date_created
            } for query in posts]

            response_data = {
                'posts': posts_list,
                'pagination': {
                    'current_page': page,
                    'next_page': page + 1 if posts_pagination.has_next else None,
                    'previous_page': page - 1 if posts_pagination.has_prev else None,
                    'per_page': per_page,
                    'total_posts': posts_pagination.total
                }
            }

            return jsonify(response_data)
        except Exception as e:
            print(e)  # Log the error
            return jsonify({'error': 'An error occurred', 'message': str(e)}), 500

    except Exception as e:
        print(e)
        return jsonify({'error': 'مشکلی پیش اومده لطفا دوباره امتحان کنید !', 'message': str(e)}), 500

# Route to list all files
@files_bp.route('/Files/Edit', methods=['PUT'])
@jwt_required()
def files_edit():
    try:
        # Get JSON data from the request
        request_data = request.get_json()
        post_id = request_data.get('id')

        # Validate post ID
        if not post_id:
            return jsonify({'error': 'Post ID is required'}), 400

        # Fetch the post from the database
        post = Posts.query.filter(Posts.id == post_id).first()
        if not post:
            return jsonify({'error': 'Post not found'}), 404


        if 'status' in request_data:
            post.status = request_data['status']

        if 'phone' in request_data:
            post.number = request_data['phone']

        if 'city' in request_data:
            post.city = request_data['city']

        if 'mahal' in request_data:
            post.mahal = request_data['mahal']

        if 'type' in request_data:
            post.type = request_data['type']

        if 'title' in request_data:
            post.title = request_data['title']

        if 'desck' in request_data:
            post.desck = request_data['desck']

        if 'Images' in request_data:
            post.Images = request_data['Images']

        if 'price' in request_data:
            post.price = request_data['price']

        if 'price_two' in request_data:
            post.price_two = request_data['price_two']

        if 'meter' in request_data:
            post.meter = request_data['meter']

        if 'Otagh' in request_data:
            post.Otagh = request_data['Otagh']

        if 'Make_years' in request_data:
            post.Make_years = request_data['Make_years']

        if 'floor' in request_data:
            post.floor = request_data['floor']

        if 'dwelling_units_per_floor' in request_data:
            post.dwelling_units_per_floor = request_data['dwelling_units_per_floor']

        if 'dwelling_unit_floor' in request_data:
            post.dwelling_unit_floor = request_data['dwelling_unit_floor']

        if 'wc' in request_data:
            post.wc = request_data['wc']

        if 'floor_type' in request_data:
            post.floor_type = request_data['floor_type']

        if 'water_provider' in request_data:
            post.water_provider = request_data['water_provider']

        if 'cool' in request_data:
            post.cool = request_data['cool']

        if 'heat' in request_data:
            post.heat = request_data['heat']

        if 'building_directions' in request_data:
            post.building_directions = request_data['building_directions']

        # Update boolean fields
        for field in ['PARKING', 'ELEVATOR', 'CABINET', 'BALCONY']:
            if field in request_data:
                setattr(post, field, bool(request_data[field]))

        neighberhood_text = Neighborhood.query.filter_by(id=post.mahal).first()
        type_text = Types_file.query.filter_by(id=post.type).first()
        city_text = Cities.query.filter_by(id=post.city).first()

        post.mahal_text = neighberhood_text.name
        post.type_text = type_text.name
        post.city_text = city_text.name
        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Post updated successfully'}), 200

    except Exception as e:
        print(e)  # Log the error for debugging
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500


@files_bp.route('/Files/Map/<int:post_id>', methods=['POST'])
@jwt_required()
def map_lat_lang(post_id):
    try:

            query = Posts.query.filter(Posts.id == post_id).first()

            if query is None:
                return jsonify({'message': 'Post not found'}), 404

            response_data = {}

            if query.map:
                try:
                    sanitized_map_string = query.map.replace("'", '"')

                    map_data = json.loads(sanitized_map_string)  # Parse JSON from the text column


                    widgets = map_data.get('widgets')
                    if widgets and isinstance(widgets, list) and len(widgets) > 0:
                        first_widget = widgets[0]
                        if isinstance(first_widget, dict) and first_widget.get('widget_type') == 'MAP_ROW':
                            data = first_widget.get('data')
                            if isinstance(data, dict):
                                location = data.get('location')
                                if isinstance(location, dict) and location.get('type') == 'FUZZY':
                                    fuzzy_data = location.get('fuzzy_data')
                                    if isinstance(fuzzy_data, dict):
                                        point = fuzzy_data.get('point')
                                        if isinstance(point, dict):
                                            response_data['latitude'] = point.get('latitude')
                                            response_data['longitude'] = point.get('longitude')
                                        else:
                                            response_data['latitude'] = None
                                            response_data['longitude'] = None
                                    else:
                                        response_data['latitude'] = None
                                        response_data['longitude'] = None
                                else:
                                    response_data['latitude'] = None
                                    response_data['longitude'] = None
                            else:
                                response_data['latitude'] = None
                                response_data['longitude'] = None
                        else:
                            response_data['latitude'] = None
                            response_data['longitude'] = None
                    else:
                        response_data['latitude'] = None
                        response_data['longitude'] = None
                except (KeyError, AttributeError, TypeError, json.JSONDecodeError) as e:
                    print(f"Error extracting coordinates: {e}")
                    response_data['latitude'] = None
                    response_data['longitude'] = None
            else:
                response_data['latitude'] = None
                response_data['longitude'] = None

            return jsonify(response_data)


    except Exception as e:
        print(e)
        return jsonify({'error': 'مشکلی پیش اومده لطفا دوباره امتحان کنید !', 'message': str(e)}), 500

@files_bp.route('/Files/Access', methods=['GET'])
@jwt_required()
def users_access():
    try:

        classifications = db.session.query(Classification).all()


        results = []
        for classification in classifications:
            results.append({
                'id': classification.id,
                'name': classification.name,
                'created_at': classification.created_at.strftime('%Y-%m-%d %H:%M:%S') if classification.created_at else None,
                'updated_at': classification.updated_at.strftime('%Y-%m-%d %H:%M:%S') if classification.updated_at else None
            })

        if results is None:
            return make_response(jsonify({
                'status': 'error',
                'message': 'An error occurred while fetching data'
            }), 500)

        return make_response(jsonify({
            'status': 'success',
            'data': results
        }), 200)

    except Exception as e:
        return make_response(jsonify({
            'status': 'error',
            'message': "error"
        }), 500)


