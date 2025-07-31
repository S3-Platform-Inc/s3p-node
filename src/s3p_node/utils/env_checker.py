import os

class EnvironmentChecker:
    """
    Проверяет и готовит инфраструктурные зависимости среды (каталоги, файлы и пр.).
    """

    def __init__(self, dependencies: list[str] = None, make: bool = False):
        if dependencies is None:
            dependencies = [
                os.environ.get("PATH_TO_PROJECT_DIR"),
                os.environ.get("SPP_ABSOLUTE_PATH_TO_PLUGIN_ARCHIVE"),
                os.environ.get("SPP_ABSOLUTE_PATH_TO_LOCAL_STORAGE"),
                os.path.join(os.environ.get("SPP_ABSOLUTE_PATH_TO_LOCAL_STORAGE"), os.environ.get("LS_WORK_DIR")),
                os.environ.get("SPP_LOG_TEMP_PATH"),
                os.environ.get("SPP_LOG_FILE_PATH"),
            ]
        self.dependencies = dependencies
        self.make = make

    def ensure(self):
        """
        Проверяет наличие всех нужных директорий и создает их при необходимости.
        """
        if self.make:
            for directory in self.dependencies:
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
        else:
            for directory in self.dependencies:
                assert os.path.exists(directory), f"Directory does not exist: {directory}"
