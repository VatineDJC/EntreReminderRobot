from datetime import datetime
from distutils.debug import DEBUG
import os
import logging
import re
from logging.handlers import TimedRotatingFileHandler

class RobotLogger:

    def setup_log(self,log_filename: str) -> logging.Logger:
        format = "[%(asctime)s] [%(levelname)s] - %(module)s.%(funcName)s (%(filename)s:%(lineno)d) - %(message)s"
        logging.basicConfig(
            filename=log_filename,
            filemode="w",
            level=logging.INFO,
            format=format,
            encoding="utf-8",
        )
        return logging.getLogger()

# The singleton
logger = RobotLogger().setup_log("./log/logs/robot.log")