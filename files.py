from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Classifictions_FOR_Factors, users_admin, PER_Classifictions_FOR_Factors, Classification
from datetime import datetime


files_bp = Blueprint('files', __name__)
#-----------------------------------------------------
# Create and list and Delete and details of Cluster
#-----------------------------------------------------
# Route to list and search Cluster
@files_bp.route('/Files/List', methods=['POST'])
@jwt_required()
def files_list():
    pass