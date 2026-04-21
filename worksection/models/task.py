from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from worksection.models.model import Model
from worksection.models.user import User
from worksection.models.custom_value import CustomValue

if TYPE_CHECKING:
    from worksection.models.project import Project


@dataclass
class Task(Model):
    id: int = 0
    name: str = ''
    text: str = ''
    page: str = ''
    status: str = ''
    priority: int = 0
    user_from: Optional[User] = None
    user_to: Optional[User] = None
    project: Optional['Project'] = None
    date_added: str = ''
    date_start: str = ''
    date_end: str = ''
    time_end: str = ''
    max_time: str = ''
    max_money: str = ''
    tags: List = field(default_factory=list)
    custom_fields: List[CustomValue] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        from worksection.models.project import Project
        obj = cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            text=data.get('text', ''),
            page=data.get('page', ''),
            status=data.get('status', ''),
            priority=data.get('priority', 0),
            date_added=data.get('date_added', ''),
            date_start=data.get('date_start', ''),
            date_end=data.get('date_end', ''),
            time_end=data.get('time_end', ''),
            max_time=data.get('max_time', ''),
            max_money=data.get('max_money', ''),
            tags=data.get('tags', []),
        )
        if data.get('user_from'):
            obj.user_from = User.from_dict(data['user_from'])
        if data.get('user_to'):
            obj.user_to = User.from_dict(data['user_to'])
        if data.get('project'):
            obj.project = Project.from_dict(data['project'])
        obj.custom_fields = [CustomValue.from_dict(f) for f in data.get('custom_fields', [])]
        return obj