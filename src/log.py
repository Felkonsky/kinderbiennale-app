__author__ = 'Felix A. Goebel'

import logging

# Logging format and configuration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
)