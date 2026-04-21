from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


class HttpResponse:
    def __init__(self, status: int, headers: Dict[str, str], body: bytes):
        self.status = status
        self.headers = headers
        self.body = body

    def json(self) -> Any:
        return json.loads(self.body.decode('utf-8'))

    def get_header(self, name: str) -> Optional[str]:
        return self.headers.get(name.lower())

    def is_json(self) -> bool:
        ct = self.get_header('content-type') or ''
        return ct.startswith('application/json')


class Http:
    def send(
        self,
        url: str,
        method: str = 'GET',
        body: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> HttpResponse:
        req = urllib.request.Request(url, data=body, method=method)
        for key, val in (headers or {}).items():
            req.add_header(key, val)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return HttpResponse(
                    resp.status,
                    {k.lower(): v for k, v in resp.headers.items()},
                    resp.read(),
                )
        except urllib.error.HTTPError as e:
            return HttpResponse(
                e.code,
                {k.lower(): v for k, v in e.headers.items()},
                e.read(),
            )

    def stream(
        self,
        url: str,
        body: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """Return raw urllib response for streaming (caller must close)."""
        req = urllib.request.Request(url, data=body, method='POST')
        for key, val in (headers or {}).items():
            req.add_header(key, val)
        try:
            return urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as e:
            return e