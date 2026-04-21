from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from worksection.client import Client

from worksection.models.downloaded_file import DownloadedFile


class Resource:
    def __init__(self, client: 'Client'):
        self._client = client

    def _call_action(self, action: str, params: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        if self._client.has_access_token():
            return self._call_user_action(action, params)
        if self._client.has_api_key():
            return self._call_admin_action(action, params)
        raise RuntimeError('No access token or API key set')

    def _call_action_one(self, action: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        result = self._call_action(action, params)
        return result[0] if result else {}

    def _call_admin_action(self, action: str, params: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        return self._client.call_admin_action(action, params)

    def _call_admin_action_one(self, action: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        return self._client.call_admin_action_one(action, params)

    def _call_user_action(self, action: str, params: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        return self._client.call_user_action(action, params)

    def _call_user_action_one(self, action: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        return self._client.call_user_action_one(action, params)

    def _call_upload(self, action: str, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self._client.has_access_token():
            return self._client.call_user_upload(action, files)
        if self._client.has_api_key():
            return self._client.call_admin_upload(action, files)
        raise RuntimeError('No access token or API key set')

    def _call_download(self, action: str, params: Dict[str, Any] = {}, sink=None) -> DownloadedFile:
        if self._client.has_access_token():
            return self._client.call_user_download(action, params, sink)
        if self._client.has_api_key():
            return self._client.call_admin_download(action, params, sink)
        raise RuntimeError('No access token or API key set')