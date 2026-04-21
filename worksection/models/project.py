from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from worksection.models.model import Model
from worksection.models.project_user import ProjectUser
from worksection.models.custom_value import CustomValue


@dataclass
class Project(Model):
    id: int = 0
    name: str = ''
    page: str = ''
    status: str = ''
    date_added: str = ''
    date_start: str = ''
    date_end: str = ''
    max_time: str = ''
    max_money: str = ''
    tags: List = field(default_factory=list)
    options: List = field(default_factory=list)
    users: List[ProjectUser] = field(default_factory=list)
    custom_fields: List[CustomValue] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        obj = cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            page=data.get('page', ''),
            status=data.get('status', ''),
            date_added=data.get('date_added', ''),
            date_start=data.get('date_start', ''),
            date_end=data.get('date_end', ''),
            max_time=data.get('max_time', ''),
            max_money=data.get('max_money', ''),
            tags=data.get('tags', []),
            options=data.get('options', []),
        )
        obj.users = [ProjectUser.from_dict(u) for u in data.get('users', [])]
        obj.custom_fields = [CustomValue.from_dict(f) for f in data.get('custom_fields', [])]
        return obj