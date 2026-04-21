from __future__ import annotations

from typing import Any, Dict, List

from worksection.resource import Resource
from worksection.models.user import User
from worksection.models.user_group import UserGroup
from worksection.models.schedule import Schedule


class MembersResource(Resource):
    def list(self) -> List[User]:
        return [User.from_dict(i) for i in self._call_action('get_users')]

    def create(self, email: str, params: Dict[str, Any] = {}) -> User:
        """Optional params: first_name, last_name, title, group, department, role"""
        return User.from_dict(self._call_action_one('add_user', {'email': email, **params}))

    def groups(self) -> List[UserGroup]:
        return [UserGroup.from_dict(i) for i in self._call_action('get_user_groups')]

    def create_group(self, title: str, params: Dict[str, Any] = {}) -> UserGroup:
        """Optional params: client (1 if a contact group)"""
        return UserGroup.from_dict(self._call_action_one('add_user_group', {'title': title, **params}))

    def schedule(self, params: Dict[str, Any] = {}) -> Dict[int, Schedule]:
        """Optional params: users (list of emails), datestart, dateend"""
        arr = self._call_action('get_users_schedule', params)
        schedules = [Schedule.from_dict(i) for i in arr]
        return {s.id: s for s in schedules}

    def update_schedule(self, data: Dict[str, Any]) -> None:
        """data: schedule data keyed by user email"""
        self._call_action('update_users_schedule', {'data': data})