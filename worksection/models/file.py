from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from worksection.models.model import Model
from worksection.models.user import User


@dataclass
class File(Model):
    id: int = 0
    page: str = ''
    name: str = ''
    size: int = 0
    date_added: str = ''
    user_from: Optional[User] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'File':
        obj = cls(
            id=data.get('id', 0),
            page=data.get('page', ''),
            name=data.get('name', ''),
            size=data.get('size', 0),
            date_added=data.get('date_added', ''),
        )
        if data.get('user_from'):
            obj.user_from = User.from_dict(data['user_from'])
        return obj