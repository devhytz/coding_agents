from flask import Blueprint, jsonify, request

from app.dtos.user_dto import UserCreateDTO, UserPatchDTO
from app.services.user_service import UserService

users_bp = Blueprint("users", __name__, url_prefix="/api/users")
service = UserService()


@users_bp.post("")
def create_user():
    dto = UserCreateDTO.from_dict(request.get_json(silent=True))
    user = service.create_user(dto)
    return jsonify(user.to_dict()), 201


@users_bp.get("")
def list_users():
    return jsonify([u.to_dict() for u in service.list_users()]), 200


@users_bp.get("/<int:user_id>")
def get_user(user_id):
    return jsonify(service.get_user(user_id).to_dict()), 200


@users_bp.put("/<int:user_id>")
def replace_user(user_id):
    dto = UserCreateDTO.from_dict(request.get_json(silent=True))
    return jsonify(service.replace_user(user_id, dto).to_dict()), 200


@users_bp.patch("/<int:user_id>")
def patch_user(user_id):
    dto = UserPatchDTO.from_dict(request.get_json(silent=True))
    return jsonify(service.patch_user(user_id, dto).to_dict()), 200


@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    service.delete_user(user_id)
    return "", 204
