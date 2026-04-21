from __future__ import annotations

from dataclasses import dataclass

from worksection.models.model import Model


@dataclass
class ProjectUser(Model):
    id: int = 0
    name: str = ''
    email: str = ''