from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from worksection.models.model import Model
from worksection.models.user import User


@dataclass
class Comment(Model):
    id: int = 0
    text: str = ''
    date_added: str = ''
    user_from: Optional[User] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        obj = cls(
            id=data.get('id', 0),
            text=data.get('text', ''),
            date_added=data.get('date_added', ''),
        )
        if data.get('user_from'):
            obj.user_from = User.from_dict(data['user_from'])
        return obj