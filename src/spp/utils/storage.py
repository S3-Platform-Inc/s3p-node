from __future__ import annotations

from hashlib import sha224
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.spp.types import SPP_document


def hashed_document_filename(doc: SPP_document, pad: str = ""):
    """

    :param doc:
    :type doc:
    :param pad:
    :type pad:
    """

    concat_name = doc.title + '_' + doc.web_link + '_' + str(doc.pub_date.timestamp())

    name: str = str(sha224(concat_name.encode('utf8')).hexdigest()) + f"_{doc.title}_{str(doc.pub_date.timestamp())}"
    if pad:
        name += f"_({pad})"

    return str(
        sha224(concat_name.encode('utf8')).hexdigest()) + f"_{doc.title}_{str(doc.pub_date.timestamp())}_({pad})"
