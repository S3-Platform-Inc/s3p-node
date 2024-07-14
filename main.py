"""
DRAFT

Главный файл

Запускает платформу.
"""
import os
from logging import config

from dotenv import load_dotenv

load_dotenv('.env')
config.fileConfig(os.environ.get('SPP_LOG_FILE_PATH'))

if __name__ == "__main__":
    from src.s3p_node import S3PApp
    spp = S3PApp()
    spp.run()
