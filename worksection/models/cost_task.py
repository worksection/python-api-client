from __future__ import annotations

from dataclasses import dataclass

from worksection.models.model import Model


@dataclass
class CostTask(Model):
    id: int = 0
    name: str = ''
    page: str = ''
    status: str = ''
    priority: int = 0
    time: str = ''
    money: str = ''