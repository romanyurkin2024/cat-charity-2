from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.core.constants import (FULL_AMOUNT_TOO_LOW, NOT_UNIQUE_NAME,
                                PROJECT_CLOSED, PROJECT_HAS_INVESTMENTS,
                                PROJECT_NOT_FOUND)


async def check_name_duplicate(
    project_name: str, session: AsyncSession
) -> None:
    if await charity_project_crud.get_project_id_by_name(
        project_name, session
    ) is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NOT_UNIQUE_NAME,
        )


async def check_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND,
        )
    return project


def check_project_not_closed(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_CLOSED,
        )


def check_full_amount(project: CharityProject, full_amount: int) -> None:
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FULL_AMOUNT_TOO_LOW,
        )


def check_project_has_no_investments(project: CharityProject) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_HAS_INVESTMENTS,
        )
