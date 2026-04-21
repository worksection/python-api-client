from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from worksection.models.model import Model


@dataclass
class CustomField(Model):
    id: int = 0
    type: str = ''
    name: str = ''
    descr: str = ''
    options: List = field(default_factory=list)