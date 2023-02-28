import os
from dotenv import load_dotenv
import logging

LOGGER = logging.getLogger(__name__)

# Load .ENV file
# After this, you can access to environment like os.environ.get("VAR")
def load_config(env_file_path: str) -> None:
    if os.path.isfile(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
    else:
        LOGGER.warning(f".ENV file does not exist on {env_file_path}")
