from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from worksection.models.model import Model
from worksection.models.user import User
from worksection.models.task import Task


@dataclass
class Cost(Model):
    id: int = 0
    comment: str = ''
    time: str = ''
    money: str = ''
    date: str = ''
    is_timer: int = 0
    user_from: Optional[User] = None
    task: Optional[Task] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Cost':
        obj = cls(
            id=data.get('id', 0),
            comment=data.get('comment', ''),
            time=data.get('time', ''),
            money=data.get('money', ''),
            date=data.get('date', ''),
            is_timer=data.get('is_timer', 0),
        )
        if data.get('user_from'):
            obj.user_from = User.from_dict(data['user_from'])
        if data.get('task'):
            obj.task = Task.from_dict(data['task'])
        return obj