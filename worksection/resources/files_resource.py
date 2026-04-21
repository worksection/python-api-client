from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from worksection.resource import Resource
from worksection.models.file import File
from worksection.models.uploaded_file import UploadedFile
from worksection.models.downloaded_file import DownloadedFile


class FilesResource(Resource):
    def list(self, params: Dict[str, Any] = {}) -> List[File]:
        """Requires id_task or id_project in params"""
        if not params.get('id_task') and not params.get('id_project'):
            raise ValueError('Either id_task or id_project is required.')
        return [File.from_dict(i) for i in self._call_action('get_files', params)]

    def download(self, file_id: int, sink=None) -> DownloadedFile:
        """sink: file path string or writable binary file object"""
        return self._call_download('download', {'id_file': file_id}, sink)

    def upload(self, file_paths: List[str]) -> List[UploadedFile]:
        """file_paths: list of local file paths to upload"""
        files = [{'key': 'files[]', 'path': path} for path in file_paths]
        return [UploadedFile.from_dict(i) for i in self._call_upload('upload_files', files)]