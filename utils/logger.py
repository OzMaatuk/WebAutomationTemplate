import logging
from config.settings import Settings

logger = logging.getLogger(__name__)
logger.setLevel(Settings().LOG_LEVEL)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)