import logging
from app.client.context import config

format = '%(asctime)s %(name)s %(levelname)s %(message)s'
fmt = logging.Formatter(format)
level = config['logger']['level']
logging.basicConfig(format=format, level=level, filename=config['logger']['path'])
log = logging.getLogger('clinet')
console_handler = logging.StreamHandler()
console_handler.setLevel(level)
console_handler.setFormatter(fmt)
log.addHandler(console_handler)
