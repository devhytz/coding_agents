from app.extensions import db
from app.models.user import User


class UserRepository:
    def get_by_id(self, user_id: int):
        return db.session.get(User, user_id)

    def get_by_email(self, email: str):
        return db.session.query(User).filter_by(email=email).first()

    def get_by_username(self, username: str):
        return db.session.query(User).filter_by(username=username).first()

    def list(self):
        return db.session.query(User).order_by(User.id).all()

    def add(self, user: User):
        db.session.add(user)
        db.session.commit()
        return user

    def save(self, user: User):
        db.session.commit()
        return user

    def delete(self, user: User):
        db.session.delete(user)
        db.session.commit()
