from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from .. import models
from ..services.auth import get_current_user
from ..services.messages import MessagesService

router = APIRouter(
    prefix='/messages',
    tags=['messages'],
)

@router.get(
    '/',
    response_model=List[models.Message],
)
def get_messages(
        user: models.User = Depends(get_current_user),
        messages_service: MessagesService = Depends(),
):
    return messages_service.get_many(user.id)

@router.post(
    '/',
    response_model=models.Message,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
        message_data: models.MessageCreate,
        user: models.User = Depends(get_current_user),
        message_service: MessagesService = Depends(),
):
    return message_service.create(
        user.id,
        message_data,
    )

@router.get(
    '/{message_id}',
    response_model=models.Message,
)
def get_operation(
        message_id: int,
        user: models.User = Depends(get_current_user),
        message_service: MessagesService = Depends(),
):
    return message_service.get(
        user.id,
        message_id,
    )

@router.put(
    '/{message_id}',
    response_model=models.Message,
)
def update_message(
        message_id: int,
        message_data: models.MessageUpdate,
        user: models.User = Depends(get_current_user),
        message_service: MessagesService = Depends(),
):
    return message_service.update(
        user.id,
        message_id,
        message_data,
    )

@router.delete(
    '/{message_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_message(
        message_id: int,
        user: models.User = Depends(get_current_user),
        messages_service: MessagesService = Depends(),
):
    messages_service.delete(
        user.id,
        message_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)