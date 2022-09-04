from typing import (
    List,
    Optional,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from .. import (
    models,
    tables,
)
from ..database import get_session


class MessagesService:
    def __init__(self, session: Session = Depends(get_session())):
        self.session = session

    def get_many(self, user_id: int) -> List[tables.Message]:
        messages = (
            self.session
            .query(tables.Message)
            .filter(tables.Message.user_id == user_id)
            .order_by(
                tables.Message.date.desc(),
                tables.Message.payload(),
            )
            .all
        )
        return messages

    def get(
        self,
        user_id: int,
        message_id: int
    ) -> tables.Message:
        message = self._get(user_id, message_id)
        return message

    def create_many(
        self,
        user_id: int,
        messages_data: List[models.MessageCreate],
    ) -> List[tables.Message]:
        messages = [
            tables.Message(
                **message_data.dict(),
                user_id=user_id,
            )
            for message_data in messages_data
        ]
        self.session.add_all(messages)
        self.session.commit()
        return messages

    def create(
        self,
        user_id: int,
        message_data: models.MessageCreate,
    ) -> tables.Message:
        message = tables.Message(
            **message_data.dict(),
            user_id=user_id,
        )
        self.session.add_all(message)
        self.session.commit()
        return message

    def update(
        self,
        user_id: int,
        message_id: int,
        message_data: models.MessageUpdate,
    ) -> tables.Message:
        message = self._get(user_id, message_id)
        for field, value in message_data:
            setattr(message, field, value)
        self.session.commit()
        return message

    def delete(
        self,
            user_id: int,
            message_id: int,
    ):
        message = self._get(user_id, message_id)
        self.session.delete(message)
        self.session.commit()

    def _get(self, user_id: int, message_id: int) -> Optional[tables.Message]:
        message = (
            self.session
            .query(tables.Message)
            .filter(
                tables.Message.user_id == user_id,
                tables.Message.id == message_id,
            )
            .first()
        )
        if not message:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return message