from __future__ import annotations

import hashlib
import hmac
import json
import os
import shutil
import time
import urllib.parse
import uuid
from typing import Any, Dict, List, Optional, Union

from worksection.exception import WorksectionException
from worksection.exceptions.response_exception import ResponseException
from worksection.exceptions.unauthorized_exception import UnauthorizedException
from worksection.http import Http
from worksection.models.downloaded_file import DownloadedFile
from worksection.oauth import Oauth

from worksection.resources.comments_resource import CommentsResource
from worksection.resources.contacts_resource import ContactsResource
from worksection.resources.costs_resource import CostsResource
from worksection.resources.events_resource import EventsResource
from worksection.resources.files_resource import FilesResource
from worksection.resources.members_resource import MembersResource
from worksection.resources.projects_resource import ProjectsResource
from worksection.resources.tasks_resource import TasksResource
from worksection.resources.timers_resource import TimersResource
from worksection.resources.user_resource import UserResource
from worksection.resources.webhook_resource import WebhookResource

_TOKEN_ACCESS = 1
_TOKEN_API_KEY = 2

_ADMIN_PATH = '/api/admin/v2'
_USER_PATH = '/api/oauth2'


class Client:
    VERSION = '2.1.0'

    def __init__(self, origin: str):
        self.origin = origin.rstrip('/')
        self._token: Dict[str, Any] = {}
        self._oauth_config: Optional[Dict[str, Any]] = None
        self._http = Http()
        self._cached_resources: Dict[str, Any] = {}

    # ── auth setup ──────────────────────────────────────────────────────────

    def set_client(self, config: Dict[str, Any]) -> 'Client':
        if not config.get('client_id'): raise WorksectionException('client_id is required.')
        if not config.get('client_secret'): raise WorksectionException('client_secret is required.')
        if not config.get('redirect_uri'): raise WorksectionException('redirect_uri is required.')
        if 'scope' in config and not isinstance(config['scope'], list):
            raise WorksectionException('scope must be a list.')
        self._oauth_config = config
        self._cached_resources = {}
        return self

    def get_oauth(self) -> Oauth:
        if not self._oauth_config:
            raise WorksectionException('OAuth client not configured. Call set_client() first.')
        return Oauth(self._oauth_config)

    def set_access_token(self, token: Union[str, Dict[str, Any]]) -> 'Client':
        if isinstance(token, str):
            self._token = {'type': _TOKEN_ACCESS, 'access_token': token}
        elif isinstance(token, dict):
            if not token.get('access_token'): raise WorksectionException('access_token is required.')
            self._token = {'type': _TOKEN_ACCESS, **token}
        else:
            raise WorksectionException('invalid token.')
        return self

    def set_api_key(self, api_key: str) -> 'Client':
        self._token = {'type': _TOKEN_API_KEY, 'api_key': api_key}
        return self

    def get_access_token(self) -> str:
        if self._token.get('type') != _TOKEN_ACCESS: raise WorksectionException('access_token not set')
        return self._token.get('access_token', '')

    def has_access_token(self) -> bool:
        return self._token.get('type') == _TOKEN_ACCESS and bool(self._token.get('access_token'))

    def get_refresh_token(self) -> str:
        if self._token.get('type') != _TOKEN_ACCESS: raise WorksectionException('access_token not set')
        return self._token.get('refresh_token', '')

    def has_refresh_token(self) -> bool:
        return self._token.get('type') == _TOKEN_ACCESS and bool(self._token.get('refresh_token'))

    def unset_refresh_token(self) -> 'Client':
        if self.has_refresh_token(): self._token['refresh_token'] = ''
        return self

    def get_api_key(self) -> str:
        if self._token.get('type') != _TOKEN_API_KEY: raise WorksectionException('api_key not set')
        return self._token.get('api_key', '')

    def has_api_key(self) -> bool:
        return self._token.get('type') == _TOKEN_API_KEY and bool(self._token.get('api_key'))

    # ── resource accessors ───────────────────────────────────────────────────

    @property
    def oauth(self) -> Oauth:
        return self.get_oauth()

    @property
    def user(self) -> UserResource:
        return self._resource('user', UserResource)

    @property
    def members(self) -> MembersResource:
        return self._resource('members', MembersResource)

    @property
    def tasks(self) -> TasksResource:
        return self._resource('tasks', TasksResource)

    @property
    def projects(self) -> ProjectsResource:
        return self._resource('projects', ProjectsResource)

    @property
    def comments(self) -> CommentsResource:
        return self._resource('comments', CommentsResource)

    @property
    def costs(self) -> CostsResource:
        return self._resource('costs', CostsResource)

    @property
    def timers(self) -> TimersResource:
        return self._resource('timers', TimersResource)

    @property
    def contacts(self) -> ContactsResource:
        return self._resource('contacts', ContactsResource)

    @property
    def events(self) -> EventsResource:
        return self._resource('events', EventsResource)

    @property
    def files(self) -> FilesResource:
        return self._resource('files', FilesResource)

    @property
    def webhook(self) -> WebhookResource:
        return self._resource('webhook', WebhookResource)

    def _resource(self, name: str, cls):
        if name not in self._cached_resources:
            self._cached_resources[name] = cls(self)
        return self._cached_resources[name]

    # ── URL builders ─────────────────────────────────────────────────────────

    def get_admin_token(self, action: str) -> str:
        if not self.has_api_key(): raise WorksectionException('API key not set')
        t = int(time.time())
        sig = hmac.new(self.get_api_key().encode(), f'{action}:{t}'.encode(), hashlib.sha256).hexdigest()
        return f'{t}_{sig}'

    def _admin_url(self, action: str) -> str:
        return f'{self.origin}{_ADMIN_PATH}?' + urllib.parse.urlencode({'action': action})

    def _user_url(self, action: str) -> str:
        return f'{self.origin}{_USER_PATH}?' + urllib.parse.urlencode({'action': action})

    # ── core send ────────────────────────────────────────────────────────────

    def _send_json(self, url: str, params: Dict[str, Any] = {}, extra_headers: Dict[str, str] = {}, retry: int = 0) -> Dict[str, Any]:
        body = json.dumps(params, ensure_ascii=False).encode('utf-8') if params else None
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'Sdk-Client': f'python-sdk:{self.VERSION}',
            **extra_headers,
        }
        resp = self._http.send(url, method='POST', body=body, headers=headers)

        if resp.status == 401:
            try:
                data = resp.json()
            except Exception:
                data = {}
            message = data.get('errorDescription') or data.get('message') or 'Unauthorized'
            if self.has_refresh_token() and 'token is expired' in message and retry == 0:
                token = self.get_oauth().fetch_access_token_by_refresh_token(self.get_refresh_token())
                self.set_access_token(token)
                updated = {**extra_headers, 'Authorization': f'Bearer {self.get_access_token()}'}
                return self._send_json(url, params, updated, retry + 1)
            raise UnauthorizedException(message)

        try:
            data = resp.json()
        except Exception:
            raise ResponseException('Invalid response body', resp.status)

        if resp.status != 200:
            raise ResponseException.from_data(data, resp.status)

        return data

    def _process(self, data: Dict[str, Any], action: str) -> Any:
        if data.get('status') == 'error':
            raise ResponseException(f"{action}: {data.get('message', 'Unknown error')}")
        return data.get('data', data)

    # ── admin / user action helpers ──────────────────────────────────────────

    def call_admin_action(self, action: str, params: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        result = self._process(
            self._send_json(self._admin_url(action), params, {'Authorization': f'Admin {self.get_admin_token(action)}'}),
            action,
        )
        return result if isinstance(result, list) else [result]

    def call_admin_action_one(self, action: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        result = self._process(
            self._send_json(self._admin_url(action), params, {'Authorization': f'Admin {self.get_admin_token(action)}'}),
            action,
        )
        return result[0] if isinstance(result, list) else result

    def call_user_action(self, action: str, params: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        result = self._process(
            self._send_json(self._user_url(action), params, {'Authorization': f'Bearer {self.get_access_token()}'}),
            action,
        )
        return result if isinstance(result, list) else [result]

    def call_user_action_one(self, action: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        result = self._process(
            self._send_json(self._user_url(action), params, {'Authorization': f'Bearer {self.get_access_token()}'}),
            action,
        )
        return result[0] if isinstance(result, list) else result

    # ── uploads ──────────────────────────────────────────────────────────────

    def call_admin_upload(self, action: str, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self._send_upload(self._admin_url(action), files, action, {'Authorization': f'Admin {self.get_admin_token(action)}'})

    def call_user_upload(self, action: str, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self._send_upload(self._user_url(action), files, action, {'Authorization': f'Bearer {self.get_access_token()}'})

    def _send_upload(self, url: str, files: List[Dict[str, Any]], action: str, extra_headers: Dict[str, str] = {}) -> List[Dict[str, Any]]:
        boundary = uuid.uuid4().hex
        body = self._build_multipart(files, boundary)
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Accept': 'application/json',
            'Sdk-Client': f'python-sdk:{self.VERSION}',
            **extra_headers,
        }
        resp = self._http.send(url, method='POST', body=body, headers=headers)
        try:
            data = resp.json()
        except Exception:
            raise ResponseException('Invalid response body', resp.status)
        if resp.status != 200:
            raise ResponseException.from_data(data, resp.status)
        result = self._process(data, action)
        return result if isinstance(result, list) else [result]

    @staticmethod
    def _build_multipart(files: List[Dict[str, Any]], boundary: str) -> bytes:
        body = b''
        for f in files:
            if not f.get('path') and not f.get('content'):
                raise WorksectionException('File path or content is required')
            key = f.get('key', 'files')
            name = f.get('name') or os.path.basename(f['path'])
            if f.get('content'):
                content = f['content'] if isinstance(f['content'], bytes) else f['content'].read()
            else:
                with open(f['path'], 'rb') as fh:
                    content = fh.read()
            body += f'--{boundary}\r\n'.encode()
            body += f'Content-Disposition: form-data; name="{key}"; filename="{name}"\r\n'.encode()
            body += b'Content-Type: application/octet-stream\r\n\r\n'
            body += content
            body += b'\r\n'
        body += f'--{boundary}--\r\n'.encode()
        return body

    # ── downloads ────────────────────────────────────────────────────────────

    def call_admin_download(self, action: str, params: Dict[str, Any] = {}, sink=None) -> DownloadedFile:
        return self._download(self._admin_url(action), params, sink, {'Authorization': f'Admin {self.get_admin_token(action)}'})

    def call_user_download(self, action: str, params: Dict[str, Any] = {}, sink=None) -> DownloadedFile:
        return self._download(self._user_url(action), params, sink, {'Authorization': f'Bearer {self.get_access_token()}'})

    def _download(self, url: str, params: Dict[str, Any] = {}, sink=None, extra_headers: Dict[str, str] = {}) -> DownloadedFile:
        body = json.dumps(params, ensure_ascii=False).encode('utf-8') if params else None
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': '*/*',
            'Sdk-Client': f'python-sdk:{self.VERSION}',
            **extra_headers,
        }
        raw = self._http.stream(url, body=body, headers=headers)

        content_type = (raw.headers.get('Content-Type') or raw.headers.get('content-type') or '')
        if content_type.startswith('application/json'):
            data = json.loads(raw.read())
            raise ResponseException(data.get('message', 'Unknown download error'))

        content_disposition = (raw.headers.get('Content-Disposition') or raw.headers.get('content-disposition') or '')
        if not content_disposition:
            raise ResponseException('Failed to download file')

        if sink is not None:
            if isinstance(sink, str):
                with open(sink, 'wb') as fh:
                    shutil.copyfileobj(raw, fh)
            else:
                shutil.copyfileobj(raw, sink)
        else:
            raw.read()

        raw.close()
        parsed = self._parse_content_disposition(content_disposition)
        return DownloadedFile.from_dict(parsed)

    @staticmethod
    def _parse_content_disposition(header: str) -> Dict[str, str]:
        import re
        result: Dict[str, str] = {}
        parts = header.split(';', 1)
        result['type'] = parts[0].strip().lower()
        if len(parts) < 2:
            return result
        for m in re.finditer(r'([a-zA-Z0-9_*]+)=(".*?"|[^;]*)', parts[1]):
            key = m.group(1).lower()
            value = m.group(2).strip().strip('"\'')
            if key.endswith('*'):
                sub = value.split("'", 2)
                if len(sub) == 3:
                    value = urllib.parse.unquote(sub[2])
                key = key[:-1]
            result[key] = value
        return result