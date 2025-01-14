from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Neighborhood, db, Neighborhoods_For_Scrapper
from datetime import datetime


classification_bp = Blueprint('classification', __name__)


# Route to list and search classification
@classification_bp.route('/Classification/List', methods=['POST'])
@jwt_required()
def classification_list():
    pass

# Route to create classification
@classification_bp.route('/Classification/Add', methods=['POST'])
@jwt_required()
def classification_create():
    pass

# Route to delete classification
@classification_bp.route('/Classification/Delete', methods=['Delete'])
@jwt_required()
def classification_delete():
    pass

# Route to add neighborhoods to classification
@classification_bp.route('/Classification/Neighborhoods/Add', methods=['POST'])
@jwt_required()
def classification_add_neighborhoods():
    pass

# Route to delete neighborhoods from classification
@classification_bp.route('/Classification/Neighborhoods/Delete', methods=['Delete'])
@jwt_required()
def classification_delete_neighborhoods():
    pass


# Route to add neighborhoods to Type
@classification_bp.route('/Classification/Type/Add', methods=['POST'])
@jwt_required()
def classification_add_type():
    pass

# Route to delete neighborhoods from Type
@classification_bp.route('/Classification/Type/Delete', methods=['Delete'])
@jwt_required()
def classification_delete_type():
    pass