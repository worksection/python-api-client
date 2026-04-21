from __future__ import annotations

from dataclasses import dataclass

from worksection.models.model import Model


@dataclass
class TagGroup(Model):
    id: int = 0
    title: str = ''
    type: str = ''
    access: str = ''