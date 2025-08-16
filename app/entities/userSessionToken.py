from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from app.entities.base import Base

class UserSessionToken(Base):
    __tablename__ = "user_session_token"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign key to users table
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    token: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    token_expiry: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationship to User
    users = relationship("User", back_populates="userSessionToken")
