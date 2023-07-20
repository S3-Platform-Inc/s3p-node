import base64


def pack(text: str, encoding='utf8') -> str:
    return base64.b64encode(text.encode(encoding)).decode(encoding)


def unpack(text: str, encoding='utf8') -> str:
    return base64.b64decode(text.encode(encoding)).decode(encoding)
