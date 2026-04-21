from __future__ import annotations

from dataclasses import dataclass

from worksection.models.model import Model


@dataclass
class Tag(Model):
    id: int = 0
    title: str = ''
    color: str = ''
    group: str = ''