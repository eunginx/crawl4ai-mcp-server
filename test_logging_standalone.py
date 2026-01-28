#!/usr/bin/env python3
"""
Quick test to verify logging setup works independently.
This will create a test log file to verify the logging configuration.
"""

import logging
import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

def test_logging_setup():
    """Test the logging setup independently."""
    # Create logs directory
    logs_dir = Path(__file__).parent / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for log filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = logs_dir / f"test_logging_{timestamp}.log"
    
    # Configure logger
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = RotatingFileHandler(
        log_filename, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Test logging
    logger.info("=== Test Logging Started ===")
    logger.info("This is a test log message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.info("=== Test Logging Complete ===")
    
    print(f"✅ Test log created: {log_filename}")
    print("✅ Check the logs directory for the test log file")
    
    return log_filename

if __name__ == "__main__":
    test_logging_setup()
