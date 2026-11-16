from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    comment: Mapped[str | None] = mapped_column(Text)
