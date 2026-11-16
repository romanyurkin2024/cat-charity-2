from typing import Any


NOT_UNIQUE_NAME = 'Проект с таким именем уже существует!'
PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'
FULL_AMOUNT_TOO_LOW = (
    'Нелья установить значение full_amount меньше уже вложенной суммы.'
)
PROJECT_HAS_INVESTMENTS = (
    'В проект были внесены средства, не подлежит удалению!'
)
ResponsesType = dict[int | str, dict[str, Any]]
PROJECT_NOT_FOUND = 'Проект не найден!'

DETAIL_SCHEMA = {
    'type': 'object',
    'properties': {'detail': {'type': 'string'}},
}


def error_response(
    description: str, examples: dict[str, tuple[str, str]] | None = None
) -> dict[str, Any]:
    content: dict[str, Any] = {'schema': DETAIL_SCHEMA}
    if examples:
        content['examples'] = {
            key: {'summary': summary, 'value': {'detail': detail}}
            for key, (summary, detail) in examples.items()
        }
    return {
        'description': description,
        'content': {'application/json': content},
    }


NOT_FOUND = error_response('The project does not exist')

CREATE_RESPONSES: ResponsesType = {
    400: error_response(
        'Not unique name',
        {'notUniqueName': ('Not unique name', NOT_UNIQUE_NAME)},
    ),
}

UPDATE_RESPONSES: ResponsesType = {
    400: error_response(
        'Invalid operations',
        {
            'fullAmountTooLow': (
                'Full amount lower than invested amount',
                FULL_AMOUNT_TOO_LOW,
            ),
            'notUniqueName': ('Not unique name', NOT_UNIQUE_NAME),
            'projectClosed': ('Project closed', PROJECT_CLOSED),
        },
    ),
    404: NOT_FOUND,
}

DELETE_RESPONSES: ResponsesType = {
    400: error_response(
        'Нельзя удалять закрытый проект или проект, '
        'в который уже были инвестированы средства.',
        {
            'projectClosed': ('Project closed', PROJECT_HAS_INVESTMENTS),
            'projectWithDonations': (
                'Project with donations', PROJECT_HAS_INVESTMENTS
            ),
        },
    ),
    404: NOT_FOUND,
}