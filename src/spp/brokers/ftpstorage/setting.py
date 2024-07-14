import os
from dataclasses import dataclass


@dataclass
class Setting:
    PASSV_ADDR: str = os.environ.get('FS_HOST')
    FTP_USER: str = os.environ.get('FS_FTP_USER')
    FTP_PASS: str = os.environ.get('FS_FTP_PASS')
    WORK_DIR: str = os.environ.get('FS_WORK_DIR')
    BLOCKSIZE: int = int(os.environ.get('FS_BLOCKSIZE', 8192))  # [default: 8192]

setting = Setting()
