"""
Logging Configuration Module
Sets up logging for the trading bot
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging(log_dir: str = "logs", log_level: str = "INFO") -> None:
    """
    Configure logging for the application
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"trading_bot_{timestamp}.log"
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Create formatters
    file_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # File handler (detailed logs)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler (less verbose)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)  # Only show warnings and errors in console
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Log the initialization
    logging.info("="*80)
    logging.info("TRADING BOT SESSION STARTED")
    logging.info(f"Log file: {log_file}")
    logging.info(f"Log level: {log_level}")
    logging.info("="*80)
    
    return str(log_file)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
