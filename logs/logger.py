import sys
import logging
from typing import Optional

class Logger:
    """logs info, warning and error message
       
       Arg:
         - name: the name of the logger
    """
    def __init__(self, name: Optional[str] = __name__) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        s_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(
            "./logs/log.log", mode="w"
        )
        fmt = logging.Formatter(
            "%(name)s:%(levelname)s - %(message)s"
        )

        s_handler.setFormatter(fmt)
        f_handler.setFormatter(fmt)

        s_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)

        self.logger.addHandler(s_handler)
        self.logger.addHandler(f_handler)
    
    def info(self, message: str) -> None:
        self.logger.info(message)
    
    def warn(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message, exc_info=True)
        sys.exit(1)