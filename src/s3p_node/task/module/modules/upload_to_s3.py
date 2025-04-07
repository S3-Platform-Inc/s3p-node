import contextlib

from src.s3p_node.task.bus import Bus
from src.s3p_node.task.module.base_module import BaseModule
from s3p_sdk.types import S3PDocument


class UploadToS3(BaseModule):
    """
    Модуль загрузки в S3 Bucket
    """

    def __init__(self, bus: Bus):
        super().__init__(bus)

        counter = 0
        for doc in self.bus.documents.data:
            if self.has(doc):
                self._upload(doc)
                self.logger.debug(f"{doc} uploaded to the s3 bucket")
                counter += 1
            else:
                self.logger.warning(f'Source id: {self.bus.source.data.id} name: {self.bus.source.data.name}.'
                                    f'Bus have not file for {doc}')

        self.logger.info(f'Updated {counter} documents.'
                         f' There are {len(self.bus.documents.data) - counter} broken documents.')

    def _upload(self, doc: S3PDocument):
        target_asset_name = doc.hash.hex()
        with self.bus.s3.open(doc, target_asset_name, mode='wb') as file, self.asset(doc) as asset:
            # Define chunk size (e.g., 1MB per chunk)
            chunk_size = 1 * 1024 * 1024  # 1MB

            while True:
                chunk = asset.read(chunk_size)  # Read next chunk
                if not chunk:
                    break  # End of file
                file.write(chunk)  # Write chunk to S3
            doc.storage = str(self.bus.s3.path_for(doc, target_asset_name))
            self.logger.info(f'Upload document title:{doc.title}, pubdate:{doc.published}, link:{doc.link} to s3:{doc.storage}')

    @contextlib.contextmanager
    def asset(self, document: S3PDocument):
        with open(self.bus.temporary_directory / document.hash.hex(), mode='rb') as file:
            yield file

    def has(self, document: S3PDocument) -> bool:
        return (self.bus.temporary_directory / document.hash.hex()).is_file()
