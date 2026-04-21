from __future__ import annotations

from dataclasses import dataclass

from worksection.models.model import Model


@dataclass
class UserGroup(Model):
    id: int = 0
    title: str = ''
    type: str = ''
    client: bool = False