# Длины полей
NAME_MIN_LENGTH = 5
NAME_MAX_LENGTH = 100
DESCRIPTION_MIN_LENGTH = 10

# Пользователи
MIN_PASSWORD_LENGTH = 3
JWT_LIFETIME_SECONDS = 3600

# Тексты ошибок
NOT_UNIQUE_NAME = 'Проект с таким именем уже существует!'
PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'
FULL_AMOUNT_TOO_LOW = (
    'Нелья установить значение full_amount меньше уже вложенной суммы.'
)
PROJECT_HAS_INVESTMENTS = (
    'В проект были внесены средства, не подлежит удалению!'
)
PROJECT_NOT_FOUND = 'Проект не найден!'
USER_DELETE_FORBIDDEN = 'Удаление пользователей запрещено!'
PASSWORD_TOO_SHORT = (
    f'Пароль должен быть не короче {MIN_PASSWORD_LENGTH} символов.'
)
PASSWORD_CONTAINS_EMAIL = 'Пароль не должен содержать e-mail.'
