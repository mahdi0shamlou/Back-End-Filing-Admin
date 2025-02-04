from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import db, Posts, Neighborhood, Types_file, Cities
from sqlalchemy import or_



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

        # Update fields if provided in the request
        if 'is_active' in request_data:
            post.is_active = request_data['is_active']

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

        if 'details' in request_data:
            post.Make_years = request_data['details']

        # Update boolean fields
        for field in ['PARKING', 'ELEVATOR', 'CABINET', 'BALCONY']:
            if field in request_data:
                setattr(post, field, bool(request_data[field]))

        # Update details and date
        if 'details' in request_data:
            post.details = request_data['details']
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
