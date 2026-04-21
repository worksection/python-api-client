from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from worksection.models.model import Model


@dataclass
class Schedule(Model):
    id: int = 0
    email: str = ''
    name: str = ''
    group: str = ''
    department: str = ''
    dates: Dict[str, str] = field(default_factory=dict)