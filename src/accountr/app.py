from fastapi import FastAPI

from . import api


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация',
    },
    {
        'name': 'messages',
        'description': 'Создание, редактирование, удаление и просмотр 10 последних сообщений',
    },

]

app = FastAPI(
    title='Accountr',
    description='Простой мессенджер с историей в 10 сообщений',
    version='1.0.0',
    openapi_tags=tags_metadata,
)

app.include_router(api.router)
