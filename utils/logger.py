# Central logging and error handling

# utils/logger.py

import logging
import os

def setup_logger():
    """
    Set up the logger to log information and errors.
    Logs are saved to the 'logs' directory.
    """
    log_dir = './data/logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'pipeline.log')

    # Create a custom logger
    logger = logging.getLogger("uk_sponsor_pipeline")
    logger.setLevel(logging.DEBUG)

    # Create handlers
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logger set up successfully!")
