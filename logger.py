import logging

logging.basicConfig(filemode="a")

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

handler = logging.FileHandler("logs.txt")

handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger.addHandler(handler)
