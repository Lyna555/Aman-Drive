from flask import Blueprint
from controllers import user_controller

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/users/<int:user_id>', methods=['GET'])(user_controller.get_user)
user_bp.route('/users', methods=['POST'])(user_controller.create_user)

user_bp.route('/login', methods=['POST'])(user_controller.login)