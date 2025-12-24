from loguru import logger
import sys

def setup_logging():
    logger.remove()

    logger.add(
        sys.stdout, 
        level="INFO", 
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{file}:{line}</cyan> | "
            "<magenta>{function}</magenta> | "
            "{message} | "
            "<yellow>{extra}</yellow>"
        ),
    )
