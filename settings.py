import os
from dotenv import load_dotenv

load_dotenv()

SEND_INTERVAL = int(os.getenv('SEND_INTERVAL', 60))
EVENT_LIMIT_SIZE = int(os.getenv('EVENT_LIMIT_SIZE', 1024 * 100))
BUTCH_LIMIT_SIZE = int(os.getenv('BUTCH_LIMIT_SIZE', 1024 * 1024 * 10))
MAXIMUM_NUMBER_EVENTS = int(os.getenv('MAXIMUM_NUMBER_EVENTS', 1000))
