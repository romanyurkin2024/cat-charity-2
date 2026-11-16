from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        return await session.get(self.model, obj_id)

    async def get_multi(self, session: AsyncSession):
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def get_not_fully_invested(self, session: AsyncSession):
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return result.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: User | None = None,
        commit: bool = True,
    ):
        obj_data = obj_in.model_dump()
        if user is not None:
            obj_data['user_id'] = user.id
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        if commit:
            await session.commit()
        else:
            await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession):
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
