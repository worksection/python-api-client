from __future__ import annotations

from typing import Any, Dict, List

from worksection.resource import Resource
from worksection.models.project import Project
from worksection.models.project_group import ProjectGroup
from worksection.models.tag import Tag
from worksection.models.tag_group import TagGroup
from worksection.models.custom_field import CustomField


class ProjectsResource(Resource):
    def list(self, params: Dict[str, Any] = {}) -> List[Project]:
        """Optional params: filter (active, pending, archived), extra (text, html, options, users)"""
        return [Project.from_dict(i) for i in self._call_action('get_projects', params)]

    def get(self, project_id: int, params: Dict[str, Any] = {}) -> Project:
        """Optional params: extra (text, html, options, users)"""
        return Project.from_dict(self._call_action_one('get_project', {'id_project': project_id, **params}))

    def create(self, title: str, params: Dict[str, Any] = {}) -> Project:
        """Optional params: email_user_from, email_manager, email_user_to, members, text,
        company, datestart, dateend, extra, max_time, max_money, tags, options.*"""
        return Project.from_dict(self._call_action_one('post_project', {'title': title, **params}))

    def update(self, project_id: int, params: Dict[str, Any] = {}) -> Project:
        """Optional params: email_manager, email_user_to, members, title, datestart, dateend,
        extra, max_time, max_money, tags, options.*"""
        return Project.from_dict(self._call_action_one('update_project', {'id_project': project_id, **params}))

    def close(self, project_id: int) -> None:
        self._call_action('close_project', {'id_project': project_id})

    def activate(self, project_id: int) -> None:
        self._call_action('activate_project', {'id_project': project_id})

    def add_members(self, project_id: int, members: List[str]) -> None:
        self._call_action('add_project_members', {'id_project': project_id, 'members': members})

    def remove_members(self, project_id: int, members: List[str]) -> None:
        self._call_action('delete_project_members', {'id_project': project_id, 'members': members})

    def groups(self) -> List[ProjectGroup]:
        return [ProjectGroup.from_dict(i) for i in self._call_action('get_project_groups')]

    def create_group(self, title: str) -> ProjectGroup:
        return ProjectGroup.from_dict(self._call_action_one('add_project_group', {'title': title}))

    def tags(self, params: Dict[str, Any] = {}) -> List[Tag]:
        """Optional params: group, type, access"""
        return [Tag.from_dict(i) for i in self._call_action('get_project_tags', params)]

    def create_tag(self, group: str, title: str) -> Tag:
        return Tag.from_dict(self._call_action_one('add_project_tags', {'group': group, 'title': title}))

    def update_tags(self, project_id: int, add_ids: List[int] = [], remove_ids: List[int] = []) -> None:
        self._call_action('update_project_tags', {
            'id_project': project_id,
            'plus': ','.join(str(i) for i in add_ids),
            'minus': ','.join(str(i) for i in remove_ids),
        })

    def tag_groups(self, params: Dict[str, Any] = {}) -> List[TagGroup]:
        """Optional params: type, access"""
        return [TagGroup.from_dict(i) for i in self._call_action('get_project_tag_groups', params)]

    def create_tag_group(self, title: str, access: str) -> TagGroup:
        """access: 'public' or 'private'"""
        result = self._call_action('add_project_tag_groups', {'title': title, 'access': access})
        return TagGroup.from_dict(result[0] if result else {})

    def custom_fields(self) -> List[CustomField]:
        return [CustomField.from_dict(i) for i in self._call_action('get_project_custom_fields')]