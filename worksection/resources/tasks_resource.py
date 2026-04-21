from __future__ import annotations

from typing import Any, Dict, List

from worksection.resource import Resource
from worksection.models.task import Task
from worksection.models.tag import Tag
from worksection.models.tag_group import TagGroup
from worksection.models.custom_field import CustomField
from worksection.models.uploaded_file import UploadedFile


class TasksResource(Resource):
    def list(self, project_id: int = 0, params: Dict[str, Any] = {}) -> List[Task]:
        """Optional params: extra (text,html,files,comments,relations,subtasks,archive), filter=active"""
        if project_id:
            return [Task.from_dict(i) for i in self._call_action('get_tasks', {'id_project': project_id, **params})]
        return [Task.from_dict(i) for i in self._call_action('get_all_tasks', params)]

    def get(self, task_id: int, params: Dict[str, Any] = {}) -> Task:
        """Optional params: extra (text, html, files, comments, relations, subtasks, subscribers, custom_fields)"""
        return Task.from_dict(self._call_action_one('get_task', {'id_task': task_id, **params}))

    def create(self, project_id: int, title: str, params: Dict[str, Any] = {}) -> Task:
        """Optional params: id_parent, email_user_from, email_user_to, priority, text, todo,
        datestart, dateend, subscribe, mention, hidden, max_time, max_money, tags, files"""
        params = dict(params)
        if isinstance(params.get('files'), list):
            params['files'] = [f.to_dict() for f in params['files'] if isinstance(f, UploadedFile) and f.id]
        else:
            params.pop('files', None)
        return Task.from_dict(self._call_action_one('post_task', {'id_project': project_id, 'title': title, **params}))

    def update(self, task_id: int, params: Dict[str, Any] = {}) -> Task:
        """Optional params: email_user_to, priority, title, datestart, dateend, dateclosed, max_time, max_money, tags"""
        return Task.from_dict(self._call_action_one('update_task', {'id_task': task_id, **params}))

    def complete(self, task_id: int) -> None:
        self._call_action('complete_task', {'id_task': task_id})

    def reopen(self, task_id: int) -> None:
        self._call_action('reopen_task', {'id_task': task_id})

    def search(self, params: Dict[str, Any]) -> List[Task]:
        """At least one of: id_project, id_task, email_user_from, email_user_to, filter"""
        return [Task.from_dict(i) for i in self._call_action('search_tasks', params)]

    def subscribe(self, task_id: int, email: str) -> None:
        self._call_action('subscribe', {'id_task': task_id, 'email_user': email})

    def unsubscribe(self, task_id: int, email: str) -> None:
        self._call_action('unsubscribe', {'id_task': task_id, 'email_user': email})

    def tags(self, params: Dict[str, Any] = {}) -> List[Tag]:
        """Optional params: group, type, access"""
        return [Tag.from_dict(i) for i in self._call_action('get_task_tags', params)]

    def create_tag(self, group: str, title: str) -> Tag:
        return Tag.from_dict(self._call_action_one('add_task_tags', {'group': group, 'title': title}))

    def update_tags(self, task_id: int, add_ids: List[int] = [], remove_ids: List[int] = []) -> None:
        self._call_action('update_task_tags', {
            'id_task': task_id,
            'plus': ','.join(str(i) for i in add_ids),
            'minus': ','.join(str(i) for i in remove_ids),
        })

    def tag_groups(self, params: Dict[str, Any] = {}) -> List[TagGroup]:
        """Optional params: type, access"""
        return [TagGroup.from_dict(i) for i in self._call_action('get_task_tag_groups', params)]

    def create_tag_group(self, title: str, type: str, access: str) -> TagGroup:
        """type: 'status' or 'label'. access: 'public' or 'private'"""
        result = self._call_action('add_task_tag_groups', {'title': title, 'type': type, 'access': access})
        return TagGroup.from_dict(result[0] if result else {})

    def custom_fields(self) -> List[CustomField]:
        return [CustomField.from_dict(i) for i in self._call_action('get_task_custom_fields')]