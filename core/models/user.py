from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post


class User(Base):

    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] 

    posts: Mapped[list["Post"]] = relationship(back_populates="user")