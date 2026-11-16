from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class InvestmentBase(CommonMixin, Base):
    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    close_date: Mapped[datetime | None] = mapped_column(DateTime)
