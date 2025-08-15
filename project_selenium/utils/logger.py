#logger.py

import logging
import os
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """
    按模块名创建 logger，每个模块可独立记录日志
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        log_dir = os.path.join(os.path.dirname(__file__), '..', 'log')
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
