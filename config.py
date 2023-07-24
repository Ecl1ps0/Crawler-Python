import logging

link_collector_logger = logging.getLogger("link_collector.py")
link_handler_logger = logging.getLogger("link_handler.py")

link_collector_logger.setLevel(logging.INFO)
link_handler_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

link_collector_logger.addHandler(file_handler)
link_collector_logger.addHandler(console_handler)

link_handler_logger.addHandler(file_handler)
link_handler_logger.addHandler(console_handler)
