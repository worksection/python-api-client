from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from worksection.models.model import Model


@dataclass
class UploadedFile(Model):
    id: str = ''
    ext: str = ''
    name: str = ''
    icon: Optional[str] = None
    error: Optional[str] = None