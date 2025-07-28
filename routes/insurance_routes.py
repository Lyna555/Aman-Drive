from flask import Blueprint
from controllers import insurance_controller

insurance_bp = Blueprint('insurance_bp', __name__, url_prefix='/insurances')

insurance_bp.route('/', methods=['GET'])(insurance_controller.get_all_insurances)
insurance_bp.route('/<int:insurance_id>', methods=['GET'])(insurance_controller.get_insurance)
insurance_bp.route('/', methods=['POST'])(insurance_controller.create_insurance)
insurance_bp.route('/<int:insurance_id>', methods=['PUT'])(insurance_controller.update_insurance)
insurance_bp.route('/<int:insurance_id>', methods=['DELETE'])(insurance_controller.delete_insurance)
