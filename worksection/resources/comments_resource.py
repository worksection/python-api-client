from __future__ import annotations

from typing import Any, Dict, List

from worksection.resource import Resource
from worksection.models.comment import Comment


class CommentsResource(Resource):
    def list(self, task_id: int, params: Dict[str, Any] = {}) -> List[Comment]:
        """Get comments for a task. Optional params: extra=files"""
        data = self._call_action('get_comments', {'id_task': task_id, **params})
        return [Comment.from_dict(i) for i in data]

    def create(self, task_id: int, text: str, params: Dict[str, Any] = {}) -> Comment:
        """Create a comment on a task. Optional params: email_user_from, hidden, mention"""
        data = self._call_action_one('post_comment', {'id_task': task_id, 'text': text, **params})
        return Comment.from_dict(data)