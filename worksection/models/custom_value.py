from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from worksection.models.model import Model


@dataclass
class CustomValue(Model):
    id: int = 0
    type: str = ''
    name: str = ''
    value: Any = None