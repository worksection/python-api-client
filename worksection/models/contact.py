from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from worksection.models.model import Model


@dataclass
class Contact(Model):
    id: int = 0
    first_name: str = ''
    last_name: str = ''
    name: str = ''
    title: str = ''
    url: str = ''
    group: str = ''
    email: str = ''
    phone: Optional[str] = None
    phone2: Optional[str] = None
    phone3: Optional[str] = None
    address: Optional[str] = None
    address2: Optional[str] = None
    services: Optional[List] = None
    contacts: Optional[str] = None
    data_added: Optional[str] = None