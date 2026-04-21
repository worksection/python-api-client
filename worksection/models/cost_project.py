from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from worksection.models.model import Model
from worksection.models.cost_task import CostTask


@dataclass
class CostProject(Model):
    id: int = 0
    name: str = ''
    page: str = ''
    time: str = ''
    money: str = ''
    monthly: Dict[str, Any] = field(default_factory=dict)
    tasks: Dict[int, CostTask] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CostProject':
        obj = cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            page=data.get('page', ''),
            time=data.get('time', ''),
            money=data.get('money', ''),
            monthly=data.get('monthly', {}),
        )
        obj.tasks = {t.id: t for t in [CostTask.from_dict(i) for i in data.get('tasks', [])]}
        return obj