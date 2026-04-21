from __future__ import annotations

from typing import Any, Dict, List

from worksection.resource import Resource
from worksection.models.cost import Cost
from worksection.models.cost_total import CostTotal


class CostsResource(Resource):
    def list(self, params: Dict[str, Any] = {}) -> List[Cost]:
        """Optional params: id_project, id_task, datestart, dateend, is_timer, filter"""
        return [Cost.from_dict(i) for i in self._call_action('get_costs', params)]

    def total(self, params: Dict[str, Any] = {}) -> CostTotal:
        """Optional params: id_project, id_task, datestart, dateend, is_timer, filter, extra"""
        arr = self._call_action('get_costs_total', params)
        raw = arr[0] if arr else {}
        total_data = {**(raw.get('total') or {}), 'projects': raw.get('projects', [])}
        return CostTotal.from_dict(total_data)

    def create(self, task_id: int, params: Dict[str, Any]) -> int:
        """Requires id_task and at least one of: time, money. Optional: email_user_from, is_rate, comment, date"""
        data = self._call_action_one('add_costs', {'id_task': task_id, **params})
        return data.get('id', 0)

    def update(self, costs_id: int, params: Dict[str, Any] = {}) -> None:
        """Optional params: time, money, is_rate, comment, date (DD.MM.YYYY)"""
        self._call_action('update_costs', {'id_costs': costs_id, **params})

    def delete(self, costs_id: int) -> None:
        self._call_action('delete_costs', {'id_costs': costs_id})