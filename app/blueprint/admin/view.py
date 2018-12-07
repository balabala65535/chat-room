from flask_login import current_user
from flask_restful import Resource, abort

from app.database import db_session
from app.model.models import User


class BlockUserView(Resource):
    def delete(self, user_id):
        if not current_user.is_admin:
            abort(403)
        user = User.query.get(user_id)
        if user.is_admin:
            abort(400)
        db_session.delete(user)
        db_session.commit()
        return '', 204

