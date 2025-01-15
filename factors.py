from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Factor, UserAccess, Users_in_Factors_Acsess, FactorAccess
from datetime import datetime


factors_bp = Blueprint('factors', __name__)
#-----------------------------------------------------
# Create and list and Delete and details of Cluster
#-----------------------------------------------------
# Route to list and search Cluster
@factors_bp.route('/Factor/List', methods=['POST'])
@jwt_required()
def factor_list():
    pass