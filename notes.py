from flask import request, Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, FileNotes, UserNotes, users_admin
from datetime import datetime

notes_bp = Blueprint('notes', __name__)

# Helper function to check admin status
def is_admin(user_phone):
    admin = users_admin.query.filter_by(phone=user_phone).first()
    return admin and admin.status == 1

# Route: List notes for a file
@notes_bp.route('/Notes/File/<int:file_id>', methods=['GET'])
@jwt_required()
def notes_list_for_file(file_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']
        if not is_admin(user_phone):
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        # Fetch all notes for the given file_id
        query = FileNotes.query.filter_by(file_id=file_id).all()
        notes_list = [{
            'id': note.id,
            'note': note.note,
            'created_at': note.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for note in query]

        return jsonify({
            'status': 'success',
            'data': {
                'notes': notes_list,
                'file_id': file_id
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! : {str(e)}'
        }), 500

# Route: Add a note for a file
@notes_bp.route('/Notes/File/<int:file_id>', methods=['POST'])
@jwt_required()
def add_note_for_file(file_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']
        if not is_admin(user_phone):
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        data = request.json
        note_content = data.get('note')

        if not note_content:
            return jsonify({
                'status': 'error',
                'message': 'متن یادداشت الزامی است.'
            }), 400

        new_note = FileNotes(
            note=note_content,
            file_id=file_id,
            created_at=datetime.now()
        )
        db.session.add(new_note)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'یادداشت با موفقیت اضافه شد.',
            'data': {
                'id': new_note.id,
                'note': new_note.note,
                'created_at': new_note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'file_id': file_id
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! : {str(e)}'
        }), 500

# Route: Delete a note for a file
@notes_bp.route('/Notes/File/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note_for_file(note_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']
        if not is_admin(user_phone):
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        note = FileNotes.query.get(note_id)
        if not note:
            return jsonify({
                'status': 'error',
                'message': 'یادداشت مورد نظر یافت نشد.'
            }), 404

        db.session.delete(note)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'یادداشت با موفقیت حذف شد.',
            'data': {
                'id': note_id
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! : {str(e)}'
        }), 500



# Route: List notes for a user
@notes_bp.route('/Notes/User/<int:user_id>', methods=['GET'])
@jwt_required()
def notes_list_for_user(user_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']
        if not is_admin(user_phone):
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        # Fetch all notes for the given user_id
        query = UserNotes.query.filter_by(user_id=user_id).all()
        notes_list = [{
            'id': note.id,
            'note': note.note,
            'created_at': note.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for note in query]

        return jsonify({
            'status': 'success',
            'data': {
                'notes': notes_list,
                'user_id': user_id
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! : {str(e)}'
        }), 500

# Route: Add a note for a user
@notes_bp.route('/Notes/User/<int:user_id>', methods=['POST'])
@jwt_required()
def add_note_for_user(user_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']
        if not is_admin(user_phone):
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        data = request.json
        note_content = data.get('note')

        if not note_content:
            return jsonify({
                'status': 'error',
                'message': 'متن یادداشت الزامی است.'
            }), 400

        new_note = UserNotes(
            note=note_content,
            user_id=user_id,
            created_at=datetime.now()
        )
        db.session.add(new_note)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'یادداشت با موفقیت اضافه شد.',
            'data': {
                'id': new_note.id,
                'note': new_note.note,
                'created_at': new_note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': user_id
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! : {str(e)}'
        }), 500

# Route: Delete a note for a user
@notes_bp.route('/Notes/User/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note_for_user(note_id):
    try:
        current_user = get_jwt_identity()
        user_phone = current_user['phone']
        if not is_admin(user_phone):
            return jsonify({
                'status': 'error',
                'message': 'شما دسترسی به این بخش ندارید !'
            }), 403

        note = UserNotes.query.get(note_id)
        if not note:
            return jsonify({
                'status': 'error',
                'message': 'یادداشت مورد نظر یافت نشد.'
            }), 404

        db.session.delete(note)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'یادداشت با موفقیت حذف شد.',
            'data': {
                'id': note_id
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'مشکلی پیش اومده ! : {str(e)}'
        }), 500