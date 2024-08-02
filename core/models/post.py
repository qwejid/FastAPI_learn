from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from  .mixins import UserRelationsMixin

from .base import Base


class Post(UserRelationsMixin, Base):

    _user_back_populates = 'posts'

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="", # на стороне алхимии
        server_default="", # на стороне бд
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, user_id={self.user_id})"
    
    def __repr__(self):
        return str(self)