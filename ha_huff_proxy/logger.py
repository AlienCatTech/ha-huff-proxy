import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                'app.log',
                maxBytes=1024*1024,  # 1MB
                backupCount=5
            ),
            logging.StreamHandler(sys.stdout)
        ]
    )