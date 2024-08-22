from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base

class UserDB(Base):
    __tablename__ = "user"
    # __table_args__ = {'extend_existing': True}

    id: Mapped[Base.get_intpk(self=Base)]
    user_name: Mapped[str] = mapped_column(unique=True, nullable=False)

    telegram_user_id: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column( default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column( default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[Base.get_created_at(self=Base)]
    updated_at: Mapped[Base.get_updated_at(self=Base)]

    def __init__(self, password: str, **kwargs):
        super().__init__(**kwargs)
        self.set_password(password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def verify_password(self, password: str) -> bool:
        """
        Verifying a plain-text password against the stored password hash.
        """
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.hashed_password)

    def set_password(self, password: str):
        """
        Hash the plain-text password
        """
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.hashed_password = pwd_context.hash(password)