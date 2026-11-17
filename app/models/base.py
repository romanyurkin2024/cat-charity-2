from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

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

    @declared_attr.directive
    def __table_args__(cls) -> tuple[CheckConstraint, ...]:
        return (
            CheckConstraint(
                'full_amount > 0',
                name=f'{cls.__tablename__}_full_amount_positive',
            ),
            CheckConstraint(
                'invested_amount >= 0',
                name=f'{cls.__tablename__}_invested_amount_not_negative',
            ),
            CheckConstraint(
                'invested_amount <= full_amount',
                name=f'{cls.__tablename__}_invested_not_more_than_full',
            ),
        )

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}(id={self.id}, '
            f'invested={self.invested_amount}/{self.full_amount}, '
            f'fully_invested={self.fully_invested})'
        )