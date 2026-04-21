from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from worksection.models.model import Model
from worksection.models.cost_project import CostProject


@dataclass
class CostTotal(Model):
    time: str = ''
    money: str = ''
    projects: Dict[int, CostProject] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CostTotal':
        obj = cls(
            time=data.get('time', ''),
            money=data.get('money', ''),
        )
        obj.projects = {p.id: p for p in [CostProject.from_dict(i) for i in data.get('projects', [])]}
        return obj