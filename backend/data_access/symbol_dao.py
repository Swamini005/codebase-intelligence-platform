from typing import List, Optional
from sqlalchemy.orm import Session
from backend.data_access.base import BaseDAO
from backend.models.symbol import Symbol
from backend.shared.enums import SymbolType

class SymbolDAO(BaseDAO[Symbol]):
    def __init__(self):
        super().__init__(Symbol)

    def get_by_repository(self, db: Session, repository_id: int) -> List[Symbol]:
        return db.query(self.model).filter(self.model.repository_id == repository_id).all()

    def get_by_file(self, db: Session, file_id: int) -> List[Symbol]:
        return db.query(self.model).filter(self.model.file_id == file_id).all()

    def get_by_type(self, db: Session, repository_id: int, symbol_type: SymbolType) -> List[Symbol]:
        return db.query(self.model).filter(
            self.model.repository_id == repository_id,
            self.model.symbol_type == symbol_type
        ).all()

symbol_dao = SymbolDAO()
