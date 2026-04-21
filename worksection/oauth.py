from __future__ import annotations

import urllib.parse
from typing import Dict, List, Optional

from worksection.exception import WorksectionException
from worksection.exceptions.response_exception import ResponseException
from worksection.http import Http


class Oauth:
    AUTHORIZE_URL = 'https://worksection.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://worksection.com/oauth2/token'
    REFRESH_TOKEN_URL = 'https://worksection.com/oauth2/refresh'

    AVAILABLE_SCOPES = [
        'projects_read', 'projects_write', 'tasks_read', 'tasks_write',
        'costs_read', 'costs_write', 'tags_read', 'tags_write',
        'comments_read', 'comments_write', 'files_read', 'files_write',
        'users_read', 'users_write', 'contacts_read', 'contacts_write', 'administrative',
    ]

    def __init__(self, config: dict):
        self._auth_url = config.get('auth_url', self.AUTHORIZE_URL)
        self._token_url = config.get('token_url', self.ACCESS_TOKEN_URL)
        self._refresh_url = config.get('refresh_url', self.REFRESH_TOKEN_URL)
        self._client_id = config.get('client_id', '')
        self._client_secret = config.get('client_secret', '')
        self._redirect_uri = config.get('redirect_uri', '')
        raw_scope = config.get('scope', None)
        if raw_scope:
            self._scope = [s for s in raw_scope if s in self.AVAILABLE_SCOPES]
        else:
            self._scope = ['projects_read', 'tasks_read', 'comments_read', 'files_read', 'users_read', 'contacts_read']
        self._http = Http()

    def get_authorization_url(self, state: str) -> str:
        if not self._auth_url: raise WorksectionException('Authorization URL is not set.')
        if not self._client_id: raise WorksectionException('Client ID is not set.')
        if not self._client_secret: raise WorksectionException('Client Secret is not set.')
        if not self._redirect_uri: raise WorksectionException('Redirect URI is not set.')

        params = urllib.parse.urlencode({
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'response_type': 'code',
            'redirect_uri': self._redirect_uri,
            'state': state,
            'scope': ','.join(self._scope),
        })
        return f'{self._auth_url}?{params}'

    def fetch_access_token_by_auth_code(self, code: str) -> dict:
        if not code: raise WorksectionException('Authorization code is required.')
        if not self._token_url: raise WorksectionException('Token URL is not set.')
        if not self._client_id: raise WorksectionException('Client ID is not set.')
        if not self._client_secret: raise WorksectionException('Client Secret is not set.')
        if not self._redirect_uri: raise WorksectionException('Redirect URI is not set.')

        params = urllib.parse.urlencode({
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self._redirect_uri,
        })
        resp = self._http.send(
            f'{self._token_url}?{params}',
            headers={'Cache-Control': 'no-store', 'Accept': 'application/json'},
        )
        return self._handle_token_response(resp)

    def fetch_access_token_by_refresh_token(self, refresh_token: str) -> dict:
        if not refresh_token: raise WorksectionException('Refresh token is required.')
        if not self._refresh_url: raise WorksectionException('Refresh Token URL is not set.')
        if not self._client_id: raise WorksectionException('Client ID is not set.')
        if not self._client_secret: raise WorksectionException('Client Secret is not set.')

        params = urllib.parse.urlencode({
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        })
        resp = self._http.send(
            f'{self._refresh_url}?{params}',
            headers={'Cache-Control': 'no-store', 'Accept': 'application/json'},
        )
        return self._handle_token_response(resp)

    def _handle_token_response(self, resp) -> dict:
        try:
            data = resp.json()
        except Exception:
            raise ResponseException('Invalid token response.')

        if resp.status != 200:
            raise ResponseException.from_data(data, resp.status)

        error = data.get('errorDescription') or data.get('error')
        if error:
            raise ResponseException(error)
        if not data.get('access_token'):
            raise ResponseException('Failed to get access token.')

        return data