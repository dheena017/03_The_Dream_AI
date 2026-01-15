"""
Centralized logging system for Dream AI
Provides consistent logging across all brain modules
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# Create logs directory
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log file path
LOG_FILE = LOG_DIR / f"dream_ai_{datetime.now().strftime('%Y%m%d')}.log"

# Create logger
logger = logging.getLogger("DreamAI")
logger.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger(module_name: str):
    """Get a logger for a specific module"""
    return logging.getLogger(f"DreamAI.{module_name}")

def log_error(module: str, error: Exception, context: str = ""):
    """Log an error with context"""
    logger = get_logger(module)
    logger.error(f"{context} - {type(error).__name__}: {str(error)}")

def log_info(module: str, message: str):
    """Log an info message"""
    logger = get_logger(module)
    logger.info(message)

def log_warning(module: str, message: str):
    """Log a warning"""
    logger = get_logger(module)
    logger.warning(message)

if __name__ == "__main__":
    log_info("logger", "Dream AI Logging System initialized")
    log_info("logger", f"Log file: {LOG_FILE}")
