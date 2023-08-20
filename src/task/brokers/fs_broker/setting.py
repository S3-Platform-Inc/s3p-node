import os
from dataclasses import dataclass


@dataclass
class Setting:
    # PASSV_ADDR: str = 'localhost'
    # FTP_USER: str = 'ftp'
    # FTP_PASS: str = 'password'
    # USER_DIR: str = 'ftp/'
    # WORK_DIR: str = 'spp/sources'
    # BLOCKSIZE: int = 2048  # [default: 8192]

    PASSV_ADDR: str = os.environ.get('FS_HOST')
    FTP_USER: str = os.environ.get('FS_FTP_USER')
    FTP_PASS: str = os.environ.get('FS_FTP_PASS')
    WORK_DIR: str = os.environ.get('FS_WORK_DIR')
    BLOCKSIZE: int = int(os.environ.get('FS_BLOCKSIZE'))  # [default: 8192]

    ...


setting = Setting()
