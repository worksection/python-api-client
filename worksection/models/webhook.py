from __future__ import annotations

from dataclasses import dataclass

from worksection.models.model import Model


@dataclass
class Webhook(Model):
    id: int = 0
    url: str = ''
    events: str = ''
    status: str = ''
    projects: str = ''