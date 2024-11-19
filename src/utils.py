import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name):
    return logging.getLogger(name)

def load_environment():
    load_dotenv()
    return {
        'CLAUDE_API_KEY': os.getenv('CLAUDE_API_KEY'),
        'OUTPUT_DIR': os.getenv('OUTPUT_DIR', 'output')
    }
