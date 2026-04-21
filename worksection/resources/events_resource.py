from __future__ import annotations

from typing import Any, Dict, List

from worksection.resource import Resource


class EventsResource(Resource):
    def list(self, period: str, project_id: int = 0, params: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """Get recent events/activity log. period e.g. '7d', '30d'"""
        if project_id:
            params = {**params, 'id_project': project_id}
        return self._call_action('get_events', {'period': period, **params})