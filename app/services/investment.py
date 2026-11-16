from datetime import datetime

from app.models.base import InvestmentBase


def close(obj: InvestmentBase) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.now()


def invest(
    target: InvestmentBase, sources: list[InvestmentBase]
) -> list[InvestmentBase]:
    """Распределить деньги между новым объектом и открытыми объектами."""
    changed = []
    for source in sources:
        if target.fully_invested:
            break
        amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount,
        )
        for obj in (target, source):
            obj.invested_amount += amount
            if obj.invested_amount == obj.full_amount:
                close(obj)
        changed.append(source)
    return changed
