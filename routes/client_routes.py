from flask import Blueprint
from controllers import client_controller

client_bp = Blueprint('client_bp', __name__, url_prefix='/clients')

client_bp.route('/', methods=['GET'])(client_controller.get_all_insurance_clients)
client_bp.route('/accidents', methods=['GET'])(client_controller.get_all_client_accidents)
client_bp.route('/<int:client_id>', methods=['GET'])(client_controller.get_client)
client_bp.route('/', methods=['POST'])(client_controller.create_client)
client_bp.route('/<int:client_id>', methods=['PUT'])(client_controller.update_client)
client_bp.route('/<int:client_id>', methods=['DELETE'])(client_controller.delete_client)