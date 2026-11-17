from http import HTTPStatus
from typing import Any

from app.core.constants import (FULL_AMOUNT_TOO_LOW, NOT_UNIQUE_NAME,
                                PROJECT_CLOSED, PROJECT_HAS_INVESTMENTS)

DETAIL_SCHEMA: dict[str, Any] = {
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


ResponsesType = dict[int | str, dict[str, Any]]

NOT_FOUND: dict[str, Any] = error_response('The project does not exist')

CREATE_RESPONSES: ResponsesType = {
    HTTPStatus.BAD_REQUEST: error_response(
        'Not unique name',
        {'notUniqueName': ('Not unique name', NOT_UNIQUE_NAME)},
    ),
}

UPDATE_RESPONSES: ResponsesType = {
    HTTPStatus.BAD_REQUEST: error_response(
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
    HTTPStatus.NOT_FOUND: NOT_FOUND,
}

DELETE_RESPONSES: ResponsesType = {
    HTTPStatus.BAD_REQUEST: error_response(
        'Нельзя удалять закрытый проект или проект, '
        'в который уже были инвестированы средства.',
        {
            'projectClosed': ('Project closed', PROJECT_HAS_INVESTMENTS),
            'projectWithDonations': (
                'Project with donations', PROJECT_HAS_INVESTMENTS
            ),
        },
    ),
    HTTPStatus.NOT_FOUND: NOT_FOUND,
}
