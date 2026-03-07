from flask import Blueprint, jsonify, request
from app.models import Asset, User
from app import db
from functools import wraps

api = Blueprint("api", __name__)


def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return jsonify({"error": "Authentication required"}), 401

        user = db.session.query(User).filter_by(username=auth.username).first()

        if not user or not user.check_password(auth.password):
            return jsonify({"error": "Invalid credentials"}), 401

        return f(user, *args, **kwargs)

    return decorated


@api.route("/api/assets", methods=["GET"])
@basic_auth_required
def get_assets(user):
    assets = db.session.query(Asset).order_by(Asset.id.desc()).all()

    result = []
    for asset in assets:
        result.append({
            "id": asset.id,
            "name": asset.name,
            "serial_number": asset.serial_number,
            "status": asset.status,
            "location": asset.location,
            "category": asset.category.name if asset.category else None,
            "owner": asset.owner.username if asset.owner else None
        })

    return jsonify(result)
