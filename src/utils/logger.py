import sys
from loguru import logger
from config.settings import settings

def setup_logger():
    # Remove default logger
    logger.remove()

    # Add console logger
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

    # Add file logger
    log_file = settings.LOG_PATH / "mapillary_downloader.log"
    settings.LOG_PATH.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_file,
        rotation="500 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )