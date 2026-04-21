from __future__ import annotations

from typing import Any, Dict, List

from worksection.resource import Resource
from worksection.models.webhook import Webhook


class WebhookResource(Resource):
    def list(self) -> List[Webhook]:
        return [Webhook.from_dict(i) for i in self._call_action('get_webhooks')]

    def create(self, url: str, events: List[str], params: Dict[str, Any] = {}) -> int:
        """events: post_task, post_comment, post_project, update_task, update_comment,
        update_project, delete_task, delete_comment, close_task.
        Optional params: projects, http_user, http_pass"""
        data = self._call_action_one('add_webhook', {'url': url, 'events': ','.join(events), **params})
        return data.get('id', 0)

    def delete(self, id: int) -> None:
        self._call_action('delete_webhook', {'id': id})