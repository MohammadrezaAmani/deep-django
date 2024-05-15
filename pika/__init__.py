__version__ = "1.3.2"

import logging

# Add NullHandler before importing Pika modules to prevent logging warnings
logging.getLogger(__name__).addHandler(logging.NullHandler())

# pylint: disable=C0413

