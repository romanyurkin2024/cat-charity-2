from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from app.core.constants import (DESCRIPTION_MIN_LENGTH, NAME_MAX_LENGTH,
                                NAME_MIN_LENGTH)


class CharityProjectBase(BaseModel):
    name: str | None = Field(
        None, min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH
    )
    description: str | None = Field(None, min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: PositiveInt | None = None

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ..., min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH
    )
    description: str = Field(..., min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
