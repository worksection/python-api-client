from __future__ import annotations

from dataclasses import dataclass

from worksection.models.model import Model


@dataclass
class EventObject(Model):
    id: int = 0
    type: str = ''
    page: str = ''