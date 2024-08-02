from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .user import User 

class Post(Base):

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default="", # на стороне алхимии
        server_default="", # на стороне бд
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
    )

    user: Mapped["User"] = relationship(back_populates="posts")