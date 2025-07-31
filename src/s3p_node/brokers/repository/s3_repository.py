from contextlib import contextmanager
from pathlib import Path

from multipledispatch import dispatch
from fsspec import AbstractFileSystem
from s3p_sdk.abstracts.abstract_repository import AbstaractRepository
from s3p_sdk.types import S3PRefer, S3PDocument


class S3DocumentAssetStorage(AbstaractRepository):
    def __init__(self, refer: S3PRefer, filesystem: AbstractFileSystem, bucket_name: str, asset_base_dir: str):
        self._filesystem = filesystem
        self._refer = refer
        self._bucket_name = Path(bucket_name)
        self._asset_base_dir = Path(asset_base_dir)

    @dispatch(S3PDocument, str)
    def has(self, document: S3PDocument, filename: str) -> bool:
        return self._filesystem.exists(
            's3://' + str(
                self.path_for(
                    document,
                    filename
                )
            ),
        )

    @dispatch(S3PDocument)
    def has(self, document: S3PDocument) -> bool:
        return self._filesystem.isdir(
            's3://' + str(self.dir_of(document))
        )

    @contextmanager
    def open(
            self,
            document: S3PDocument,
            filename: str,
            **kwargs,
    ):
        """Open file-like object in s3 bucket (Write-mode)"""
        with self._filesystem.open(
                's3://' + str(
                    self.path_for(
                        document,
                        filename
                    )
                ),
                **kwargs
        ) as file:
            yield file

    @property
    def _base_dir(self) -> Path:
        return self._bucket_name / self._asset_base_dir / self._refer.name / 'assets'

    def dir_of(self, document: S3PDocument) -> Path:
        return self._base_dir / document.hash.hex()

    def path_for(self, document: S3PDocument, asset: str) -> Path:
        return self.dir_of(document) / asset