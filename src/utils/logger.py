"""
Logging configuration for elevator safety inspection system
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(level=logging.INFO, log_file=None):
    """
    Configure logging for the application
    
    Args:
        level: Logging level (default: INFO)
        log_file: Path to log file (default: auto-generated based on date)
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate log filename if not provided
    if log_file is None:
        date_str = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_dir, f"elevator_safety_{date_str}.log")
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates when reconfiguring
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Configure file handler with rotation (10MB max size, keep 10 backups)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=10
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(level)
    
    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Create application-specific logger
    app_logger = logging.getLogger('elevator_safety')
    app_logger.info(f"Logging initialized at level {logging.getLevelName(level)}")
    app_logger.info(f"Log file: {log_file}")
    
    return app_logger
