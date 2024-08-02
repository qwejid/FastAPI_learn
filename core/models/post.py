from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

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