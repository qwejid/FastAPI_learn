from .base import Base
from sqlalchemy.orm import Mapped


class Product(Base):

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
