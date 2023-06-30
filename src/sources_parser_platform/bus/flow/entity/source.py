from src.sources_parser_platform.types.spp_source import SPP_source
from .. import Flow


class SPP_FE_source(Flow):
    data: SPP_source

    def __init__(self, src: SPP_source):
        super().__init__()

        self.data = src
