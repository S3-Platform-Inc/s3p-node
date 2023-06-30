from dataclasses import dataclass


@dataclass
class Setting:
    PASSV_ADDR: str = 'localhost'
    FTP_USER: str = 'ftp'
    FTP_PASS: str = 'password'
    USER_DIR: str = 'ftp/'
    WORK_DIR: str = 'spp/sources'
    BLOCKSIZE: int = 2048  # [default: 8192]

    ...


setting = Setting()
