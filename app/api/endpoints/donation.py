from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import invest

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
UserDep = Annotated[User, Depends(current_user)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(session: SessionDep):
    """Показать список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.post('/', response_model=DonationDB)
async def create_donation(
    donation: DonationCreate, session: SessionDep, user: UserDep
):
    """Создать пожертвование."""
    new_donation = await donation_crud.create(
        donation, session, user=user, commit=False
    )
    sources = await charity_project_crud.get_not_fully_invested(session)
    session.add_all(invest(new_donation, sources))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get('/my', response_model=list[DonationDB])
async def get_my_donations(session: SessionDep, user: UserDep):
    """Показать список пожертвований текущего пользователя."""
    return await donation_crud.get_by_user(user, session)
