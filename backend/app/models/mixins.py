"""Mixins reutilizaveis para modelos SQLAlchemy"""
from datetime import datetime
from sqlalchemy import Column, DateTime


class TimestampMixin:
    """Mixin que adiciona campos created_at e updated_at"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    """Mixin que adiciona campo deleted_at para soft delete"""
    deleted_at = Column(DateTime, nullable=True)
    
    @property
    def is_deleted(self):
        """Retorna True se o registro foi deletado"""
        return self.deleted_at is not None
    
    def soft_delete(self):
        """Marca o registro como deletado"""
        self.deleted_at = datetime.utcnow()
    
    def restore(self):
        """Restaura o registro deletado"""
        self.deleted_at = None
