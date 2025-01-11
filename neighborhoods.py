from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Neighborhood

neighborhoods_bp = Blueprint('neighborhoods', __name__)

@neighborhoods_bp.route('/Neighborhoods/List', methods=['POST'])
@jwt_required()
def Neighborhoods_List():
    pass