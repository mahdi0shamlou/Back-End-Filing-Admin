from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Classification, ClassificationTypes, ClassificationNeighborhood, users_admin, Neighborhood, Types_file
from datetime import datetime


cluster_bp = Blueprint('cluster', __name__)
#-----------------------------------------------------
# Create and list and Delete and details of Cluster
#-----------------------------------------------------
# Route to list and search Cluster
@cluster_bp.route('/Cluster/List', methods=['POST'])
@jwt_required()
def cluster_list():
    pass