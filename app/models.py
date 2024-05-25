from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


# Tabela de usuários - Migração para o banco MySQL
class Usuarios(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User : {self.username} >"
