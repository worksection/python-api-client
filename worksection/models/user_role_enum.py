from enum import Enum


class UserRoleEnum(str, Enum):
    Owner = 'owner'
    Admin = 'account admin'
    TeamAdmin = 'team admin'
    DepartmentAdmin = 'department admin'
    User = 'user'
    Guest = 'guest'
    Reader = 'reader'