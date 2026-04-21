from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from worksection.models.model import Model
from worksection.models.user_role_enum import UserRoleEnum


@dataclass
class User(Model):
    id: int = 0
    first_name: str = ''
    last_name: str = ''
    name: str = ''
    title: str = ''
    rate: Optional[str] = None
    avatar: str = ''
    group: str = ''
    department: str = ''
    role: str = ''
    email: str = ''
    phone: Optional[str] = None
    phone2: Optional[str] = None
    phone3: Optional[str] = None
    address: Optional[str] = None
    address2: Optional[str] = None

    def is_owner(self) -> bool: return self.role == UserRoleEnum.Owner
    def is_admin(self) -> bool: return self.role == UserRoleEnum.Admin
    def is_team_admin(self) -> bool: return self.role == UserRoleEnum.TeamAdmin
    def is_department_admin(self) -> bool: return self.role == UserRoleEnum.DepartmentAdmin
    def is_user(self) -> bool: return self.role == UserRoleEnum.User
    def is_guest(self) -> bool: return self.role == UserRoleEnum.Guest
    def is_reader(self) -> bool: return self.role == UserRoleEnum.Reader