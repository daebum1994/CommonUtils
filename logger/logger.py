import os
import logging
from logging.handlers import RotatingFileHandler

ROOT_DIR = "./"


def setup_logger(name, log_level=logging.ERROR):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 로그 디렉토리 생성
    log_dir = os.path.join(ROOT_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 로그 파일 이름 설정
    log_file = os.path.join(log_dir, f"{name}.log")

    # 파일 핸들러 설정
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(log_level)

    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 포매터 설정
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 핸들러가 중복 추가되지 않도록 확인
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# 로거 생성 예시
info_logger = setup_logger("info_logger", log_level=logging.INFO)
error_logger = setup_logger("error_logger", log_level=logging.ERROR)
