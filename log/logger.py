import logging
import os


class LoggerSetup:
    _instance = None

    def __new__(cls, log_dir="./log", log_file="error.log"):
        if cls._instance is None:
            cls._instance = super(LoggerSetup, cls).__new__(cls)
            cls._instance._initialize(log_dir, log_file)
        return cls._instance

    def _initialize(self, log_dir, log_file):
        self.log_dir = log_dir
        self.log_file = log_file

        os.makedirs(self.log_dir, exist_ok=True)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(os.path.join(self.log_dir, self.log_file))
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
