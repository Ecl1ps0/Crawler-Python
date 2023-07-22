import logging

logging.basicConfig(level=logging.ERROR, filename='logs.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
