"""
Главный файл

Запускает платформу.
"""
import argparse
import json
import os
from logging import config

from dotenv import load_dotenv

from src.s3p_node.utils.env_checker import EnvironmentChecker

load_dotenv('.env.dev')
EnvironmentChecker(make=False).ensure()

config.fileConfig(os.environ.get('SPP_LOG_FILE_PATH'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S3 Platform")
    parser.add_argument(
        "-p", "--plugin-id",
        type=int,
        help="Запуск по ID плагина"
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Использовать SimpleTaskSystem вместо DynamicTaskTrackingSystem"
    )
    parser.add_argument(
        "--plugin-json",
        type=str,
        help="JSON-строка с данными плагина для Simple режима"
    )
    parser.add_argument(
        "--plugin-file",
        type=str,
        help="Путь к JSON-файлу с описанием плагина для Simple режима"
    )

    args = parser.parse_args()

    from s3p_sdk.types import S3PPlugin
    from src.s3p_node import App


    def load_plugin_from_json(json_str: str) -> S3PPlugin:
        try:
            data = json.loads(json_str)
            return S3PPlugin(**data)
        except Exception as e:
            raise ValueError(f"Ошибка загрузки плагина: {e}")

    plugin = None
    if args.simple:
        if args.plugin_json:
            plugin = load_plugin_from_json(args.plugin_json)
        elif args.plugin_file:
            with open(args.plugin_file, encoding="utf-8") as f:
                plugin = load_plugin_from_json(f.read())
        else:
            raise RuntimeError("Для --simple необходим один из аргументов: --plugin-json или --plugin-file")

    if isinstance(plugin, S3PPlugin):
        spp = App(plugin.id)
    elif isinstance(args.plugin_id, int):
        spp = App(args.plugin_id)
    else:
        spp = App()
    spp.run()
