from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from worksection.models.model import Model
from worksection.models.user import User
from worksection.models.task import Task


@dataclass
class Timer(Model):
    id: int = 0
    time: str = ''
    date_started: str = ''
    user_from: Optional[User] = None
    task: Optional[Task] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Timer':
        obj = cls(
            id=data.get('id', 0),
            time=data.get('time', ''),
            date_started=data.get('date_started', ''),
        )
        if data.get('user_from'):
            obj.user_from = User.from_dict(data['user_from'])
        if data.get('task'):
            obj.task = Task.from_dict(data['task'])
        return obj