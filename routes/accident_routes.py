from flask import Blueprint
from controllers import accident_controller

accident_bp = Blueprint('accident_bp', __name__, url_prefix='/accidents')

accident_bp.route('/', methods=['GET'])(accident_controller.get_all_accidents)
accident_bp.route('/<int:accident_id>', methods=['GET'])(accident_controller.get_accident)
accident_bp.route('/', methods=['POST'])(accident_controller.create_accident)
accident_bp.route('/<int:accident_id>', methods=['PUT'])(accident_controller.update_accident)
accident_bp.route('/<int:accident_id>', methods=['DELETE'])(accident_controller.delete_accident)
