from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from worksection.models.model import Model
from worksection.models.event_object import EventObject
from worksection.models.event_action_enum import EventActionEnum
from worksection.models.user import User


@dataclass
class Event(Model):
    action: str = ''
    date_added: str = ''
    object: Optional[EventObject] = None
    user_from: Optional[User] = None
    new: Dict[str, Any] = field(default_factory=dict)
    old: Dict[str, Any] = field(default_factory=dict)

    def is_post(self) -> bool: return self.action == EventActionEnum.Post
    def is_update(self) -> bool: return self.action == EventActionEnum.Update
    def is_delete(self) -> bool: return self.action == EventActionEnum.Delete
    def is_task_close(self) -> bool: return self.action == EventActionEnum.TaskClose
    def is_task_reopen(self) -> bool: return self.action == EventActionEnum.TaskReopen

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        obj = cls(
            action=data.get('action', ''),
            date_added=data.get('date_added', ''),
            new=data.get('new', {}),
            old=data.get('old', {}),
        )
        if data.get('object'):
            obj.object = EventObject.from_dict(data['object'])
        if data.get('user_from'):
            obj.user_from = User.from_dict(data['user_from'])
        return obj