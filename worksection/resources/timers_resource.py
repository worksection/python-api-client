from __future__ import annotations

from typing import List

from worksection.resource import Resource
from worksection.models.timer import Timer


class TimersResource(Resource):
    def all(self) -> List[Timer]:
        return [Timer.from_dict(i) for i in self._call_admin_action('get_timers')]

    def stop(self, timer_id: int) -> None:
        self._call_admin_action('stop_timer', {'timer': timer_id})