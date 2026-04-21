from __future__ import annotations

from dataclasses import dataclass

from worksection.models.model import Model


@dataclass
class DownloadedFile(Model):
    filename: str = ''
    type: str = ''