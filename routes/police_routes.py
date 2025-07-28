from flask import Blueprint
from controllers import police_controller

police_bp = Blueprint('police_bp', __name__, url_prefix='/police')

police_bp.route('/', methods=['POST'])(police_controller.create_police)
police_bp.route('/', methods=['GET'])(police_controller.get_all_police)
police_bp.route('/accidents', methods=['GET'])(police_controller.get_all_police_accidents)
police_bp.route('/<int:police_id>', methods=['GET'])(police_controller.get_police_by_id)
police_bp.route('/<int:police_id>', methods=['PUT'])(police_controller.update_police)
police_bp.route('/<int:police_id>', methods=['DELETE'])(police_controller.delete_police)