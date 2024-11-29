import json
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from s3p_sdk.types import S3PPlugin
from s3p_sdk.plugin.types import SOURCE

from src.s3p_node.plugin.s3plugin import S3Plugin


class TestS3Plugin:

    @pytest.fixture(scope='module')
    def fix_metadata(self) -> S3PPlugin:
        return S3PPlugin(None, 'S3-Platform-Inc/s3p-plugin-parser-w3c', True, None,
                         json.loads('{"plugin": {"reference": "w3c", "type": "SOURCE", "filenames": ["w3c.py"], "localstorage": false}, "task": {"trigger": {"type": "SCHEDULE", "interval": "86400 seconds"}}, "middleware": {"modules": [{"order": 1, "name": "TimezoneSafeControl", "critical": true, "params": {}}, {"order": 2, "name": "FilterOnlyNewDocumentWithDB", "critical": true, "params": {}}, {"order": 3, "name": "SaveDocumentToDB", "critical": true, "params": {}}]}, "payload": {"file": "w3c.py", "class": "W3C", "entry": {"point": "content", "params": [{"key": "driver", "value": {"type": "module", "name": "WebDriver", "bus": true}}, {"key": "max_count_documents", "value": {"type": "const", "value": 50}}]}}}')
                         , SOURCE, None)

    @pytest.fixture(scope='module')
    def set_envs(self):
        p = Path(__file__).parent.parent.parent.parent / '.env.dev'
        print(p)
        load_dotenv(p)

    def test_load_config(self, fix_metadata, set_envs):
        sp = S3Plugin(fix_metadata)
        print(sp.config)

    def test_obtain_plugin_manifest_from_s3(self, fix_metadata, set_envs):
        sp = S3Plugin(fix_metadata)
        print(sp.manifest)

    def test_obtain_plugin_files_from_s3(self, fix_metadata, set_envs):
        sp = S3Plugin(fix_metadata)
        print(sp.must_load_files())

    def test_obtain_payload(self, fix_metadata, set_envs):
        sp = S3Plugin(fix_metadata)
        p = sp.payload
        print(p)
