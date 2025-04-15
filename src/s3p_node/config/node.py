from pathlib import Path
from multipledispatch import dispatch
import yaml

from s3p_sdk.types import S3PNode


class NodeConfig:
    _config: S3PNode

    @dispatch(S3PNode)
    def __init__(self, config: S3PNode):
        self._config = config

    @dispatch(Path)
    def __init__(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)
            self.__init__(config_dict)

    @dispatch(dict)
    def __init__(self, yaml: dict):
        self.__init__(S3PNode(**yaml))

    def content(self) -> S3PNode:
        return self._config


if __name__ == '__main__':
    out = NodeConfig(Path('test-config.yaml')).content()
    origin = S3PNode(None, "test-s3p-node", "localhost", {
            'plugins': {
                'types': ["SOURCE",],
            }
        }, None)
    print(type(out))
    print(out)
    print(origin)
    print(out == origin)
