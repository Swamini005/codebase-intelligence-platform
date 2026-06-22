from typing import Optional
from sqlalchemy.orm import Session
from backend.data_access.base import BaseDAO
from backend.models.user import User

class UserDAO(BaseDAO[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

user_dao = UserDAO()
