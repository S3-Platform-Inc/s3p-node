from .abc_plugin import ABC_Plugin


class GIT_Plugin(ABC_Plugin):

    def __init__(self, url: str):
        super().__init__(url)

        self._is_sppfile()

        ...

    def _is_sppfile(self) -> bool:
        ...