#logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str,level=logging.DEBUG) -> logging.Logger:
    """
    按模块名创建 logger，每个模块可独立记录日志
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)

        #日志目录
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        #日志文件名
        log_file = os.path.join(log_dir,f'{name}.log')

        # RotatingFileHandler
        file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*10, backupCount=10,encoding='utf-8')

        # console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
