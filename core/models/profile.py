from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

from  .mixins import UserRelationsMixin


class Profile(UserRelationsMixin, Base):

    _user_id_unique = True
    _user_back_populates = 'profile'

    first_name:Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None]
