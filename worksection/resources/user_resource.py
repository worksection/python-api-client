from __future__ import annotations

from typing import Optional

from worksection.resource import Resource
from worksection.models.user import User
from worksection.models.timer import Timer


class UserResource(Resource):
    def profile(self) -> User:
        return User.from_dict(self._call_user_action_one('me'))

    def timer(self) -> Optional[Timer]:
        arr = self._call_user_action('get_my_timer')
        return Timer.from_dict(arr[0]) if len(arr) == 1 else None

    def start_timer(self, task_id: int) -> None:
        self._call_user_action('start_my_timer', {'id_task': task_id})

    def stop_timer(self, comment: str = '') -> None:
        self._call_user_action('stop_my_timer', {'comment': comment})

    def discard_timer(self) -> None:
        self._call_user_action('delete_my_timer')