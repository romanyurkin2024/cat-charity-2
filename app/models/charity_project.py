from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestmentBase
from app.core.constants import NAME_MAX_LENGTH


class CharityProject(InvestmentBase):
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), unique=True)
    description: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f'{super().__repr__()[:-1]}, name={self.name!r})'