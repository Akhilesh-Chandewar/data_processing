import logging
from logging.handlers import RotatingFileHandler
import os

# Log directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Base log file name
LOG_FILE = "network_security.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure Rotating File Handler
handler = RotatingFileHandler(LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=5)  # 5 MB

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("network_security_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
