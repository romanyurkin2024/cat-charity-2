from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_full_amount, check_name_duplicate,
                                check_project_exists,
                                check_project_has_no_investments,
                                check_project_not_closed)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import close, invest
from app.api.responses import (CREATE_RESPONSES, DELETE_RESPONSES,
                               UPDATE_RESPONSES)


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_charity_projects(session: SessionDep):
    """Показать список всех целевых проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    responses=CREATE_RESPONSES
)
async def create_charity_project(
    charity_project: CharityProjectCreate, session: SessionDep
):
    """Создать целевой проект."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project, session, commit=False
    )
    sources = await donation_crud.get_not_fully_invested(session)
    session.add_all(invest(new_project, sources))
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    responses=UPDATE_RESPONSES,
)
async def update_charity_project(
    project_id: int, obj_in: CharityProjectUpdate, session: SessionDep
):
    """Редактировать целевой проект.

    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await check_project_exists(project_id, session)
    check_project_not_closed(project)
    if obj_in.name is not None and obj_in.name != project.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_full_amount(project, obj_in.full_amount)
        if obj_in.full_amount == project.invested_amount:
            close(project)
    return await charity_project_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    responses=DELETE_RESPONSES
)
async def delete_charity_project(project_id: int, session: SessionDep):
    """Удалить целевой проект.

    Нельзя удалить проект, в который уже были инвестированы средства.
    """
    project = await check_project_exists(project_id, session)
    check_project_has_no_investments(project)
    return await charity_project_crud.remove(project, session)
